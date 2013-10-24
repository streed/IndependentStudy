from flask import Blueprint, render_template, abort
from flask.ext.security import login_required
from flask.ext.security.decorators import roles_required, roles_accepted

rider = Blueprint( "rider", __name__, template_folder="templates" )

from ..models.schedule import Schedule

@rider.route( "/" )
@login_required
@roles_accepted( "Admin", "Rider" )
def index():

	#TODO This should be filtered and return by a different handler rather than
	#on the page itself.
	schedules = Schedule.query.all()

	scheds = []
	for s in schedules:
		scheds.append( { "driver_id": s.driver.id, "start": [ s.start.lat, s.start.lng ], "end": [ s.end.lat, s.end.lng ] } )

	return render_template( "rider/index.html", schedules=scheds )

