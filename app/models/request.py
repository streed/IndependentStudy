from ..db import db

class Request( db.Model ):
	id = db.Column( db.Integer, primary_key=True )	
	is_accepted = db.Column( db.Boolean )
	schedule_id = db.Column( db.Integer )
	rider_id = db.Column( db.Integer )
	schedule_id = db.Column( db.Integer )

	schedule = db.relationship( "Schedule", backref=db.backref( "request", lazy="dynamic" ) )
	rider = db.relationship( "Rider", backref=db.backref( "requests", lazy="dynamic" ) )

	def __init__( self, schedule, rider ):
		self.schedule = schedule
		self.rider = rider
