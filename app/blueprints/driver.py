from flask import Blueprint, render_template, abort, redirect, flash
from flask.ext.security import login_required
from flask.ext.security.core import current_user
from flask.ext.security.decorators import roles_required, roles_accepted

from ..models.account import accounts
from ..models.car import Car, CarForm
from ..models.driver import Driver
from ..models.schedule import Schedule, ScheduleForm
from ..db import db

driver = Blueprint( "driver", __name__, template_folder="templates" )

def errors( form ):
	for f, e in form.errors.items():
		flash( "%s %s" % ( getattr( form, f ).label.text, e ) )

@driver.route( "/", methods=["get","post"] )
@login_required
def index():
	if( current_user.has_role( "Driver" ) ):
		return render_template( "driver/index.html" )
	else:
		carForm = CarForm()
		if( carForm.validate_on_submit() ):
			car = Car( carForm.make.data, carForm.model.data, carForm.color.data )
			driver = Driver( carForm.license_plate.data, current_user, car, carForm.available_seats.data )
			accounts.add_role_to_user( current_user, "Driver" )
			db.session.add( car )
			db.session.add( driver )
			db.session.commit()
			return render_template( 'driver/index.html' )
		else:
			errors( carForm )
			return render_template( "driver/sign_up.html", car=carForm )

@driver.route( "/schedule" )
@login_required
def schedule():
	if( current_user.has_role( "Driver" ) ):
		return render_template( "driver/schedule.html" )
	else:
		return redirect( "/" )

@driver.route( "/schedule/new" )
@login_required
def schedule_add():
	if( current_user.has_role( "Driver" ) ):
		scheduleForm = ScheduleForm()

		if( scheduleForm.validate_on_submit() ):
			#Save schedule

			return redirect( "/schedule" )
		else:
			return render_template( "driver/schedule_add.html" )
	else:
		return redirect( "/driver" )
