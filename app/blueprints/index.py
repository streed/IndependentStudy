from flask import Blueprint, render_template, abort, redirect
from jinja2 import TemplateNotFound

from ..models.forms import AccountForm

index = Blueprint( "index", __name__, template_folder="templates" )

@index.route( "/", methods=["GET", "POST"] )
def index_page():
	accountForm = AccountForm()
	
	if accountForm.validate_on_submit():
		return redirect( "/login" )

	return render_template( "index/index.html", form=accountForm )

@index.route( "/about" )
def about():
	return render_template( "index/about.html" )

@index.route( "/registration", methods=["GET","POST"] )
def registration():
	accountForm = AccountForm()
	
	if accountForm.validate_on_submit():
		return redirect( "/login" )

	return render_template( "index/registration.html", form=accountForm )

@index.route( "/login", methods=["GET","POST"] )
def login():
	loginForm = LoginForm()

	if loginForm.validate_on_submit():
		#login
		return redirect( "/rider" )

	return render_template( "index/login.html" )
