from flask import Blueprint, render_template, abort, redirect
from flask_security.core import current_user
from jinja2 import TemplateNotFound

from ..db import accounts, db
from ..models.forms import AccountForm
from ..models.rider import Rider

index = Blueprint( "index", __name__, template_folder="templates" )

def registerValidation( accountForm ):

	if accountForm.validate_on_submit():
		#add the user to the database.
		#default is that all new users are Riders
		#TODO Change this so the form auto checks if the email is already used. Write validator
		user = accounts.find_user( email=accountForm.email.data )
		if not user:
			user = accounts.create_user( email=accountForm.email.data, password=accountForm.password.data )

			user.name = accountForm.name.data
			user.age = accountForm.age.data
			user.phone_number = accountForm.phoneNumber.data

			role = accounts.find_role( "Rider" )
			accounts.add_role_to_user( user, role )

			rider = Rider( user )
			db.session.add( rider )

			db.session.commit()

			return redirect( "/login" )
	else:
		return None

@index.route( "/", methods=["GET", "POST"] )
def index_page():	
	if( current_user.is_authenticated() ):
		return redirect( "/rider" )
	accountForm = AccountForm()
	ret = registerValidation( accountForm )

	if ret:
		return ret
	else:
		return render_template( "index/index.html", form=accountForm )

@index.route( "/about" )
def about():
	return render_template( "index/about.html" )

@index.route( "/registration", methods=["GET","POST"] )
def registration():
	accountForm = AccountForm()
	ret = registerValidation( accountForm )

	if ret:
		return ret
	else:
		return render_template( "index/registration.html", form=accountForm )

@index.route( "/login", methods=["GET","POST"] )
def login():
	loginForm = LoginForm()

	if loginForm.validate_on_submit():
		#login
		return redirect( "/rider" )

	return render_template( "index/login.html" )
