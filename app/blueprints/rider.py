from flask import Blueprint, render_template, abort, json, redirect, flash
from flask.ext.security import login_required
from flask.ext.security.core import current_user
from flask.ext.security.decorators import roles_required, roles_accepted

from ..db import db

from ..util import get_ranked_schedules

rider = Blueprint( "rider", __name__, template_folder="templates" )

from ..models.schedule import Schedule
from ..models.rider import Rider
from ..models.request import Request
from ..models.location import Location

from math import radians, sin, cos, asin, sqrt, pi, atan2
EARTH_RADIUS = 3956.0

def _get_distance( alat, alng, blat, blng ):
  alat = radians( alat )
  alng = radians( alng )
  blat = radians( blat )
  blng = radians( blng )
  dlat, dlng = ( blat - alat, blng - alng )
  a = sin( dlat / 2.0 ) ** 2.0 + cos( alat ) * cos( blat ) * sin( dlng / 2.0 ) ** 2.0
  circle = 2 * asin( min( 1, sqrt( a ) ) )
  distance = circle * EARTH_RADIUS

  return distance

def filter_by_distance( lat, lng, schedules, dist=0.5, use_start=True ):
  ret = []
  for s in schedules:
    if( use_start and _get_distance( lat, lng, s.start.lat, s.start.lng ) <= dist ):
      ret.append( s )
    if( not use_start and _get_distance( lat, lng, s.end.lat, s.end.lng ) <= dist ):
      ret.append( s )

  return ret

@rider.route( "/" )
@login_required
@roles_accepted( "Rider" )
def index():
  requests = current_user.rider[0].requests
  for r in requests:
    if( r.is_accepted and r.is_deleted ):
      flash( "Your ride from %s to %s has been accepted by %s." % ( r.schedule.start_str, r.schedule.end_str, r.schedule.driver.account.name ), "success" )
      db.session.delete( r )
  db.session.commit()
  return render_template( "rider/index.html", schedules=[] )

@rider.route( "/requests" )
@login_required
@roles_accepted( "Rider" )
def requests():
  return render_template( "rider/requests.html", requests=current_user.rider[0].requests )

@rider.route( "/accept/<int:id>/<lat>/<lng>" )
@login_required
@roles_accepted( "Rider" )
def accept( id, lat, lng ):
  #Check if the schedule already has a user or if the car is full?
  schedule = Schedule.query.filter_by( id=id ).first()
  requests = schedule.requests

  total_riders = 0
  if( requests ):
    total_riders = len( requests )

  if( total_riders + 1 <= schedule.driver.availableSeats ):
    #other riders so many need to have people walk to each other, 
    #loop through and find the closest person and have this user
    #walk to the other user.
    if( total_riders > 0 ):
      locs = [ ( r, r.loc ) for r in requests ]
      dist = float( "inf" )
      closest = None
      for l in locs:
        d = _get_distance( l[1].lat, l[1].lng, float( lat ), float( lng ) )
        if( d < dist ):
          dist = d
          closest = l[0]
      flash( "The ride you wish to take has other riders, so you will need to meet up with %s to organize a location to meet call them at %s." % ( closest.rider.account.name, closest.rider.account.phone_number ) ) 
    else:
      loc = Location.from_str( "%s,%s" % ( lat, lng ) )
      db.session.add( loc )
      db.session.commit()

      request = Request( loc )
      request.rider = current_user.rider[0]
      request.driver = schedule.driver
      request.schedule = schedule
      current_user.rider[0].requests.append( request )

      db.session.add( request )
      db.session.commit()

      day = schedule.day_str

      time = schedule.time_str

      flash( "Sent Request: To %s for a ride on %s at %s" % ( schedule.driver.account.name, day, time ), "success" )

  return redirect( "/rider" )

@rider.route( "/routes/<slat>/<slng>/<elat>/<elng>/<int:day>/<int:time>" )
@login_required
@roles_accepted( "Rider" )
def get_routes( slat, slng, elat, elng, day, time ):
  schedules = get_ranked_schedules( slat, slng, elat, elng, day, time )
  scheds = []
  for s in schedules:
    _s = Schedule.query.filter_by( id=s ).first()
    scheds.append( _s )

  starts = filter_by_distance( float( slat ), float( slng ), scheds )
  ends = filter_by_distance( float( elat ),  float( elng ), scheds, use_start=False )

  scheds = list( set( starts ) & set( ends ) )

  ret = []
  for s in scheds:
    ret.append( { "driver_name": s.driver.account.name, 
         "schedule_id": s.id, 
         "start_str": s.start_str,
         "end_str": s.end_str,
         "start": [ s.start.lat, s.start.lng ], 
         "end": [ s.end.lat, s.end.lng ] } )

  return json.dumps( ret )

