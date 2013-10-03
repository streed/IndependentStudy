from ..db import db

class Notification( db.Model ):
	id = db.Column( db.Integer, primary_key=True )
	request_id = db.Column( db.Integer, db.ForeignKey( "request.id" ) )
	from_account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )
	to_account_id = db.Column( db.Integer, db.ForeignKey( "account.id" ) )

	has_read = db.Column( db.Boolean )

	message = db.Column( db.String( 512 ) )

	from_account = db.Column( "Account", backref=db.backref( "received", lazy="dynamic" ) )
	to_account = db.Column( "Account", backref=db.backref( "sent", lazy="dynamic" ) )
	request = db.Column( "Request", backref=db.backref( "notification", lazy="dynamic" ) )
