from flask import Blueprint, render_template, abort, json, redirect, flash
from flask.ext.security import login_required
from flask.ext.security.decorators import roles_required, roles_accepted

from ..util import get_ranked_schedules

rider = Blueprint( "rider", __name__, template_folder="templates" )

from ..models.schedule import Schedule

@rider.route( "/" )
@login_required
@roles_accepted( "Rider" )
def index():
	return render_template( "rider/index.html", schedules=[] )

@rider.route( "/accept/<int:id>" )
@login_required
@roles_accepted( "Rider" )
def accept( id ):
	schedule = Schedule.query.filter_by( id=id ).first()

	day = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ][schedule.day]

	time = [ ( "%02d:%02d" % ( i // 60, i % 60 ) ) for i in range( 24 * 60 ) if i % 30 == 0][schedule.time]

	flash( "Sent Request To: %s for a ride on %s at %s" % ( schedule.driver.account.name, day, time ), "success" )

	return redirect( "/rider" )

@rider.route( "/routes/<lat>/<lng>/<day>/<time>" )
@login_required
@roles_accepted( "Rider" )
def get_routes( lat, lng, day, time ):
	schedules = get_ranked_schedules( lat, lng, day, time )
	scheds = []
	for s in schedules:
		scheds.append( { "driver_name": s.driver.account.name, 
				 "driver_id": s.driver.id, 
				 "start_str": s.start_str,
				 "end_str": s.end_str,
				 "start": [ s.start.lat, s.start.lng ], 
				 "end": [ s.end.lat, s.end.lng ] } )

	return json.dumps( scheds )

