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

@rider.route( "/" )
@login_required
@roles_accepted( "Rider" )
def index():
	return render_template( "rider/index.html", schedules=[] )

@rider.route( "/requests" )
@login_required
@roles_accepted( "Rider" )
def requests():
	return render_template( "rider/requests.html", requests=current_user.rider[0].requests )

@rider.route( "/accept/<int:id>" )
@login_required
@roles_accepted( "Rider" )
def accept( id ):
	schedule = Schedule.query.filter_by( id=id ).first()

	request = Request()
	request.rider = current_user.rider[0]
	request.driver = schedule.driver
	request.schedule = schedule
	current_user.rider[0].requests.append( request )

	db.session.add( request )
	db.session.commit()

	day = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ][schedule.day]

	time = [ ( "%02d:%02d" % ( i // 60, i % 60 ) ) for i in range( 24 * 60 ) if i % 30 == 0][schedule.time]

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

	ret = []
	for s in scheds:
		ret.append( { "driver_name": s.driver.account.name, 
				 "driver_id": s.driver.id, 
				 "start_str": s.start_str,
				 "end_str": s.end_str,
				 "start": [ s.start.lat, s.start.lng ], 
				 "end": [ s.end.lat, s.end.lng ] } )

	return json.dumps( ret )

