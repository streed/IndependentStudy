from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import TextField, IntegerField, HiddenField, SelectField
from wtforms.validators import DataRequired

from ..db import db
from .location import Location
from .driver import Driver

schedule_locations_start = db.Table( "schedule_locations_start", 
			db.Column( "schedule_id", db.Integer(), db.ForeignKey( "schedule.id" ) ),
			db.Column( "location_id", db.Integer(), db.ForeignKey( "location.id" ) ) )

schedule_locations_end = db.Table( "schedule_locations_end", 
			db.Column( "schedule_id", db.Integer(), db.ForeignKey( "schedule.id" ) ),
			db.Column( "location_id", db.Integer(), db.ForeignKey( "location.id" ) ) )

class Schedule( db.Model ):
	"""
		This encompasses the information that is needed
		to show a single schedule event.
	"""
	id = db.Column( db.Integer, primary_key=True )

	#This will be a value between 0 and 6.
	day = db.Column( db.Integer )

	#This will be a value between 0 and 86400 (the minutes in a day)
	time = db.Column( db.Integer )

	#When True this will be the in set schedule.
	#When False it is a temporary schedule and
	#will override the permanent schedule.
	is_permanent = db.Column( db.Boolean )
	
	#A schedule can be deactivated and activated.
	#This could be for out of town situations or
	#the driver cannot give any rides then.
	is_active = db.Column( db.Boolean )

	start_str = db.Column( db.String( 64 ) )
	end_str = db.Column( db.String( 64 ) )
	start = db.relationship( "Location", secondary=schedule_locations_start, backref=db.backref( "schedules_start" , lazy="dynamic" ), uselist=False )
	end = db.relationship( "Location", secondary=schedule_locations_end, backref=db.backref( "schedules_end", lazy="dynamic" ), uselist=False )
	
	driver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
	driver = db.relationship( "Driver", uselist=False )

	def __init__( self, day, time, is_permanent, is_active, driver, start_str, start, end_str, end ):
		self.day = day
		self.time = time
		self.is_permanent = is_permanent
		self.is_active = is_active
		self.driver = driver
		self.start_str = start_str
		self.start = start
		self.end_str = end_str
		self.end = end

class ScheduleForm( Form ):
	day = SelectField( 'Day', choices=[(0, "Monday"), ( 1, "Tuesday" ), ( 2, "Wednesday" ), ( 3, "Thursday" ), ( 4, "Friday" ), ( 5, "Saturday" ), ( 6, "Sunday" ) ], validators=[DataRequired()] )
	time = IntegerField( 'Time', validators=[DataRequired()] )
	start_str = TextField( "Start Location", validators=[DataRequired()] )
	end_str = TextField( "End Location", validators=[DataRequired()] )
	start = HiddenField( 'Start Location', validators=[DataRequired()] )
	end =  HiddenField( 'End Location', validators=[DataRequired()] )


