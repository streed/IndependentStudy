import sys
from app import app

if __name__ == "__main__":
	if( len( sys.argv ) >= 2 ):
		if( sys.argv[1] == "create_db" ):
			print( "Creating the database." )
			from app.db import db
			from app.models.account import *
			from app.models.car import *
			from app.models.driver import *
			from app.models.request import *
			from app.models.rider import *
			from app.models.schedule import *
			from app.models.location import *
			from app.models.route import *
			db.drop_all()
			db.create_all()
			db.create_default_roles()
		elif( sys.argv[1] == "create_data" ):
			db.create_some_example_data()
	else:
		app.run( debug=True )
