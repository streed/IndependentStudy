from flask import Blueprint, render_template, abort

rider = Blueprint( "rider", __name__, template_folder="templates" )

@rider.route( "/" )
def index():
	return render_template( "rider/index.html" )

