from flask import Blueprint, render_template, abort, redirect
from flask.ext.security import login_required
from flask.ext.security.core import current_user
from flask.ext.security.decorators import roles_required, roles_accepted

from ..db import db
from ..models.account import accounts
from ..models.car import Car, CarForm
from ..models.driver import Driver
from ..models.schedule import Schedule, ScheduleForm
from ..util import errors

from ..util import save_route

driver = Blueprint( "driver", __name__, template_folder="templates" )


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

@driver.route( "/schedule/new", methods=["get", "post"] )
@login_required
def schedule_add():
	if( current_user.has_role( "Driver" ) ):
		scheduleForm = ScheduleForm()
		if( scheduleForm.validate_on_submit() ):
			driver = Driver.query.filter_by( account=current_user ).first()
			start_str = scheduleForm.start_str.data
			start = scheduleForm.start.data
			end_str = scheduleForm.end_str.data
			end = scheduleForm.end.data

			#Convert the string representations to Actual locations.
			start = Location.from_str( start )
			end = Location.from_str( end )

			schedule = Schedule( 
						scheduleForm.day.data, 
						scheduleForm.time.data, 
						True, 
						True, 
						driver, 
						start_str,
						start,
						end_str,
						end )

			save_route( schedule )

			db.session.add( start )
			db.session.add( end )
			db.session.add( schedule )
			db.session.commit()
	
			return redirect( "/schedule" )
		else:
			errors( scheduleForm )
			return render_template( "driver/schedule_new.html", schedule=scheduleForm )
	else:
		return redirect( "/driver" )
