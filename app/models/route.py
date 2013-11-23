from ..db import db

class RouteLoc( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	lat = db.Column( db.Float() )
	lng = db.Column( db.Float() )
	direction = db.Column( db.String( 24 ) )

	route_id = db.Column( db.Integer, db.ForeignKey(  "route.id" ) )
	route = db.relationship( "Route", backref="locs", uselist=True )


	def __init__( self, lat, lng, direction, route ):
		self.lat = lat
		self.lng = lng
		self.direction = direction
		self.route = route

class Route( db.Model ):
	id = db.Column( db.Integer, primary_key=True )

	schedule_id = db.Column( db.Integer, db.ForeignKey( "schedule.id" ) )
	schedule = db.relationship( "Schedule", backref="route", uselist=False )

	dirver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
	driver = db.relationship( "Driver", backref="routes" )


