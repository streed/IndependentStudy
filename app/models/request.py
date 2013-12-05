from ..db import db

class Request( db.Model ):
	id = db.Column( db.Integer, primary_key=True )	
	is_accepted = db.Column( db.Boolean )
	driver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
	rider_id = db.Column( db.Integer, db.ForeignKey( "rider.id" ) )
	schedule_id = db.Column( db.Integer, db.ForeignKey( "schedule.id" ) )

	def __init__( self, is_accepted=False ):
		self.is_accepted = is_accepted
