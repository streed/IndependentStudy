from ..db import db

class Request( db.Model ):
	id = db.Column( db.Integer, primary_key=True )	
	is_accepted = db.Column( db.Boolean )
	rider_id = db.Column( db.Integer, db.ForeignKey( "rider.id" ) )
	schedule_id = db.Column( db.Integer, db.ForeignKey( "schedule.id" ) )

	schedule = db.relationship( "Schedule", backref=db.backref( "request", lazy="dynamic" ) )
	rider = db.relationship( "Rider", backref=db.backref( "requests", lazy="dynamic" ) )

	def __init__( self, schedule, rider ):
		self.schedule = schedule
		self.rider = rider
