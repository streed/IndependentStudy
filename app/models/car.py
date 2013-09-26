from ..db import db

class Car( db.Model ):
	id = db.Column( db.Integer, primary_key=True )

	#TODO: Switch this to a key into another table.
	make = db.Column( db.String( 80 ), unique=True )

	#TODO: Switch this to a key into another table.
	model = db.Column( db.String( 80 ), unique=True )

	#TODO: Make this better than it is.
	color = db.Column( db.String( 80 ) )

	def __init__( self, make, model, color ):
		self.make = make
		self.model = model
		self.color = color

