from flask import Blueprint, render_template, abort, redirect
from flask.ext.security import login_required
from flask.ext.security.core import current_user
from flask.ext.security.decorators import roles_required, roles_accepted

from ..models.account import accounts
from ..db import db

driver = Blueprint( "driver", __name__, template_folder="templates" )

@driver.route( "/" )
@login_required
def index():
	if( current_user.has_role( "Driver" ) ):
		return render_template( "driver/index.html" )
	else:
		accounts.add_role_to_user( current_user, "Driver" )
		db.session.commit()
		
		return render_template( "driver/sign_up.html" )

@driver.route( "/schedule" )
@login_required
def schedule():
	if( current_user.has_role( "Driver" ) ):
		return render_template( "driver/schedule.html" )
	else:
		return redirect( "/" )
