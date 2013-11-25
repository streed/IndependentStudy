from flask import Blueprint, render_template, abort, json
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

@rider.route( "/routes/<lat>/<lng>/<day>/<time>" )
@login_required
@roles_accepted( "Rider" )
def get_routes( lat, lng, day, time ):
	schedules = get_ranked_schedules( lat, lng, day, time )
	scheds = []
	for s in schedules:
		scheds.append( { "driver_id": s.driver.id, "start": [ s.start.lat, s.start.lng ], "end": [ s.end.lat, s.end.lng ] } )

	return json.dumps( scheds )

