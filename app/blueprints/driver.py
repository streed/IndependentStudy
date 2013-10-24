from flask import Blueprint, render_template, abort
from flask.ext.security import login_required
from flask.ext.security.decorators import roles_required, roles_accepted

driver = Blueprint( "driver", __name__, template_folder="templates" )

@driver.route( "/" )
@login_required
@roles_accepted( "Admin", "Driver" )
def index():
	return render_template( "driver/index.html" )

