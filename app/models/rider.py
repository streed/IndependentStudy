from ..db import db

class Rider( db.Model ):
	"""
		A rider consists of their profile information.
		Their requests.
	"""
	id = db.Column( db.Integer, primary_key=True )

	#Profile Information
	account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )
	
	account = db.relationship( "Account", backref=db.backref( "driver", lazy="dynamic" ) )

	def __init__( self, account ):
		self.account = account
