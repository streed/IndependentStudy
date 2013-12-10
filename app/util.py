import os
import json
import subprocess
from flask import flash

from .models.schedule import Schedule

_routes = {}

import numpy as np
from scipy import spatial

def _compact( l ):
	r = []
	for i in l:
		if( i not in r ):
			r.append( i )
	return r

def _stable_diff( a, b ):
	r = []
	for i in a:
		if( i in b ):
			r.append( i )

	return r

def errors( form ):
	for f, e in form.errors.items():
		flash( "%s %s" % ( getattr( form, f ).label.text, ",".join( e ) ), "error" )

def save_route( schedule ):
	path = os.path.join( os.path.dirname( __file__ ), "..", "util", "google_routes.js" )

	start = schedule.start
	end = schedule.end
	param = [ "node", path, "\"%s\"" % ( " ".join( [ str( start.lat ), str( start.lng ), str( end.lat ), str( end.lng ) ] ) ) ]

	param = " ".join( param )

	data =  subprocess.check_output( param, shell=True )

	data = data.decode( "utf-8" )

	with open( os.path.join( os.path.dirname( __file__ ), "..", "routes", "%d.json" % ( schedule.id ) ), "w" ) as f:
		f.write( data )
	
def rank_routes( routes, client=[], num=3 ):
	#Read in the data file, for now just out.json, should 
	#read in from STDIN to pipe everything together nicely.
	route_ids = []
	route_id = 0
	steps_locs = []
	route_ranges = {}
	rs = {}
	for r in routes:
		f = os.path.join( os.path.dirname( __file__ ), "..", "routes", "%d.json" % r )
		data = json.load( open( f ) )
		rs[r] =  data["routes"][0]

		routes = data["routes"]

		#KDTree expects a numpy.array so convert the points list into
		#a numpy.array for use with the KDTree
		for steps in routes:
			new_ids = [ r ] * len( steps["steps"] )
			route_ranges[r] = ( len( route_ids ), len( route_ids ) + len( new_ids ), )
			route_ids += new_ids
			steps_locs += [ [ p["loc"]["lat"], p["loc"]["lng"] ] for p in steps["steps"] ]

	steps_locs = np.array( steps_locs )

	#Build the tree using the GPS coordinates.
	tree = spatial.cKDTree( steps_locs )

	#Begin the finding of the points that are of interest
	pts = []
	for s in client:
		loc = np.array( s )

		closest = tree.query( loc, k=num )
		indexes = closest[1]	
		pts.append( _compact( [ route_ids[i] for i in indexes ] ) )

	#Ok we got all valid points that could be around the start
	#and end points. Let's find the routes that around both start and end.
	s = pts[0]
	for p in pts[1:]:
		s = _stable_diff( s, p )


	#S contains the intersection of the resultant sets
	#from both the start points and end points.
	return list( s )

def ranked_routes( slat, slng, elat, elng, day, time, num=3 ):
	#Get the ones near by the end point, this can be done in sql.
	#Take the start point and pass it to rank_routes
	ids = [ s.id for s in  Schedule.query.filter_by( day=day, time=time ).all() ]

	if( ids ):
		return rank_routes( ids, client=[ [ slat, slng ], [ elat, elng ] ], num=num )
	else:
		return None


def get_ranked_schedules( slat, slng, elat, elng, day, time ):
	ret = ranked_routes( slat, slng, elat, elng, day, time )
	return ret

