from flask import Blueprint, render_template, abort, redirect, flash
from flask.ext.security import login_required
from flask.ext.security.core import current_user
from flask.ext.security.decorators import roles_required, roles_accepted

from ..db import db
from ..models.account import accounts
from ..models.car import Car, CarForm
from ..models.driver import Driver
from ..models.location import Location
from ..models.schedule import Schedule, ScheduleForm
from ..models.request import Request
from ..util import errors, save_route

driver = Blueprint( "driver", __name__, template_folder="templates" )


@driver.route( "/", methods=["get","post"] )
@login_required
def index():
	if( current_user.has_role( "Driver" ) ):
		requests = current_user.driver[0].requests
		return render_template( "driver/index.html", requests=requests )
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
		schedules = current_user.driver[0].schedules
		return render_template( "driver/schedule.html", schedules=schedules )
	else:
		return redirect( "/" )

@driver.route( "/schedule/new", methods=["get", "post"] )
@roles_required( "Driver" )
@login_required
def schedule_add():
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


		db.session.add( start )
		db.session.add( end )
		db.session.add( schedule )
		db.session.commit()

		save_route( schedule )

		return redirect( "/driver/schedule" )
	else:
		errors( scheduleForm )
		return render_template( "driver/schedule_new.html", schedule=scheduleForm )

@driver.route( "/request/<int:id>/<method>" )
@login_required
@roles_required( "Driver" )
def request_accept( id, method ):
	request = Request.query.filter_by( id=id ).first()

	if( method == "accept" ):
		flash( "You accepted ther request to give %s a ride from %s to %s." % ( request.rider.account.name, request.schedule.start_str, request.schedule.end_str ), "success" )
		request.is_accepted = True
		request.is_deleted = True
	elif( method == "decline" ):
		flash( "You declined the request from %s." % ( request.rider.account.name ), "warning" )
		request.is_accepted = False
		request.is_deleted = False
	else:
		flash( "Incorrect parameters.", "danger" )

	db.session.add( request )
	db.session.commit()
	
	return redirect( "/driver" )

