from ..db import db
from .car import Car

class Driver( db.Model ):
	"""
		A Driver consists of their profile information.
		Their account.
		Their chedule.
		Their car.

		These are sent out to other tables and used there.
	"""
	id = db.Column( db.Integer, primary_key=True )
	license_plate = db.Column( db.String( 10 ), unique=True )
	availableSeats = db.Column( db.Integer )

	#Driver relations
	account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )
	car_id = db.Column( db.Integer, db.ForeignKey( "car.id" ) )

	account = db.relationship( "Account", backref="account", uselist=False )
	car = db.relationship( "Car", backref="driver", uselist=False )

	def __init__( self, license_plate, account, car, availableSeats ):
		self.license_plate = license_plate
		self.account = account
		self.car = car
		self.availableSeats = availableSeats
