from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from ..db import db

roles_users = db.Table( "roles_users",
		db.Column( "account_id", db.Integer(), db.ForeignKey( "account.id" ) ),
		db.Column( "role_id", db.Integer(), db.ForeignKey( "role.id" ) ) )

class Role( db.Model, RoleMixin ):
	id = db.Column( db.Integer(), primary_key=True )
	name = db.Column( db.String( 20 ), unique=True )
	description = db.Column( db.String( 255 ) )

class Account( db.Model, UserMixin ):
	"""
		Abstracting out the account details allows for people
		to be both drivers AND riders. Without this there would
		be a lot of duplication of code and things would become
		rather messy in this manner.
	"""
	id = db.Column( db.Integer, primary_key=True )
	email = db.Column( db.String( 80 ), unique=True )
	password = db.Column( db.String( 80 ) )
	name = db.Column( db.String( 80 ) )
	age = db.Column( db.Integer )
	phoneNumber = db.Column( db.String( 80 ) )
	active = db.Column( db.Boolean() )
	confirmed_at = db.Column( db.DateTime() )

	#0 -> male
	#1 -> female
	#2 -> unspecified
	#This will be mapped to a string value through a method on this
	#object.
	gender = db.Column( db.Integer )

	roles = db.relationship( "Role", secondary=roles_users, backref=db.backref( "users", lazy="dynamic" ) )

accounts = SQLAlchemyUserDatastore( db, Account, Role )
