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
			db.create_all()
	else:
		app.run( debug=True )
