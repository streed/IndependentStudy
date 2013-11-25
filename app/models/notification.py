from ..db import db

class Notification( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	has_read = db.Column( db.Boolean )
	message = db.Column( db.String( 512 ) )

	from_account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )
	to_account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )
	from_account = db.relationship( "Account", backref="received", foreign_keys=[from_account_id] )
	to_account = db.relationship( "Account", backref="sent" )
