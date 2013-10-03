from ..db import db

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

	lat = db.Column( db.Float )
	lng = db.Column( db.Float )

	driver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
	driver = db.relationship( "Driver", backref=db.backref( "schedule", lazy="dynamic" ) )

	def __init__( self, day, time, is_permanent, is_active, driver ):
		self.day = day
		self.time = time
		self.is_permanent = is_permanent
		self.is_active = is_active
		self.driver = driver



