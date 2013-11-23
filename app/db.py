from . import app
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy( app )

from .models.account import accounts

security = Security( app, accounts )

def create_default_roles():
	"""
		There are two roles currently. Admin and User.

		The Admin role only allows users marked as an admin to access admin specific
		resources.

		The User role only allows users marked as a user to access user specific
		resources.
	"""

	accounts.create_role( name="Admin", description="This marks a user as a Admin and they can only access the Admin pages and information." )
	accounts.create_role( name="Rider", description="This marks a user as a Rider" )
	accounts.create_role( name="Driver", description="This marks a user as a Driver" )

	db.session.commit()

def create_some_example_data():
	#Create a few dummy drivers.
	dr = accounts.find_role( "Driver" )
	driver = accounts.create_user( email="test_driver_1@test.com", password="pass" )
	accounts.add_role_to_user( driver, dr )

	from .models.driver import Driver
	from .models.car import Car
	car = Car( "Toyota", "Corolla", "Black" )
	db.session.add( car )

	driver = Driver( "test_plate", driver, car, 3 )
	db.session.add( driver )

	driver1 = accounts.create_user( email="test_driver_2@test.com", password="pass" )
	accounts.add_role_to_user( driver1, dr )

	driver1 = Driver( "test_plate2", driver1, car, 2 )
	db.session.add( driver1 )

	#Make some locations.
	from .models.location import Location
	start = Location( 37.297923, -80.055787 )
	end = Location( 37.290411, -80.042922 )

	end2 = Location( 37.30403, -79.964281 )

	db.session.add( start )
	db.session.add( end )
	db.session.add( end2 )

	#Create a couple schedules.
	from .models.schedule import Schedule

	sched = Schedule( 0, 14*60, True, True, driver, "Roanoke College",  start, "Valley View Mall", end )
	db.session.add( sched )


	sched = Schedule( 0, 14*60, True, True, driver1, "Kime Lane, Salem VA", start, "Valley View Mall", end2 )
	db.session.add( sched )

	db.session.commit()

db.create_default_roles = create_default_roles
db.create_some_example_data = create_some_example_data
