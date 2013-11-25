from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired
from ..db import db

class Car( db.Model ):
	id = db.Column( db.Integer, primary_key=True )

	#TODO: Switch this to a key into another table.
	make = db.Column( db.String( 80 ) )

	#TODO: Switch this to a key into another table.
	model = db.Column( db.String( 80 ) )

	#TODO: Make this better than it is.
	color = db.Column( db.String( 80 ) )

	def __init__( self, make, model, color ):
		self.make = make
		self.model = model
		self.color = color

class CarForm( Form ):
	make = TextField( 'Make', validators=[DataRequired()] )
	model = TextField( 'Model', validators=[DataRequired()] )
	color = TextField( 'Color', validators=[DataRequired()] )
	license_plate = TextField( 'License Plate', validators=[DataRequired()] )
	available_seats = IntegerField( 'Available Seats', validators=[DataRequired()] )
