import os
import subprocess
from ..db import db

class Location( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	lat = db.Column( db.Float() )
	lng = db.Column( db.Float() )

	def __init__( self, lat, lng ):
		self.lat = lat
		self.lng = lng

	@classmethod
	def from_str( cls, s ):
		lat, lng = s.split( "," )

		lat = float( lat )
		lng = float( lng )

		return Location( lat, lng )
