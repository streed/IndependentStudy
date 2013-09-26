from ..db import db

class Account( db.Model ):
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

	#0 -> male
	#1 -> female
	#2 -> unspecified
	#This will be mapped to a string value through a method on this
	#object.
	gender = db.Column( db.Integer )
