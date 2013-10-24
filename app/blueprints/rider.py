from flask import Blueprint, render_template, abort
from flask.ext.security import login_required
from flask.ext.security.decorators import roles_required, roles_accepted

rider = Blueprint( "rider", __name__, template_folder="templates" )

@rider.route( "/" )
@login_required
@roles_accepted( "Admin", "Rider" )
def index():
	return render_template( "rider/index.html" )

