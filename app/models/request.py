from ..db import db

class Request( db.Model ):
	id = db.Column( db.Integer, primary_key=True )	
	is_accepted = db.Column( db.Boolean )
	driver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
	rider_id = db.Column( db.Integer, db.ForeignKey( "rider.id" ) )
	schedule_id = db.Column( db.Integer, db.ForeignKey( "schedule.id" ) )

	schedule = db.relationship( "Schedule", backref="request", uselist=False )
	rider = db.relationship( "Rider", backref="requests" )
	driver = db.relationship( "Driver", backref="requests" )

	def __init__( self, schedule, rider, is_accepted=False ):
		self.schedule = schedule
		self.rider = rider
		self.is_accepted = is_accepted
