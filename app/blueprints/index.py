from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

index = Blueprint( "index", __name__, template_folder="templates" )

@index.route( "/" )
def index_page():
	return render_template( "index/index.html" )

@index.route( "/about" )
def about():
	return render_template( "about.html" )

@index.route( "/registration", methods=["GET","POST"] )
def registration():
	return render_template( "registration.html" )
