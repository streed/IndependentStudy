try:
	import configparser
except ImportError:
	import ConfigParser as configparser
import os
from flask import Flask

config = configparser.ConfigParser()
config.readfp( open( os.path.expanduser( "~/.independentStudy" ) ) )

app = Flask( __name__, template_folder=os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), "templates" ) )

app.debug = config.getboolean( "app", "debug" )
app.config["SQLALCHEMY_DATABASE_URI"] = config.get( "app", "database_uri" )
app.config["SECRET_KEY"] = config.get( "app", "secret_key" )

app.jinja_env.trim_blocks = True

from .blueprints.index import index
from .blueprints.driver import driver
from .blueprints.rider import rider

app.register_blueprint( index )
app.register_blueprint( driver, url_prefix="/driver" )
app.register_blueprint( rider, url_prefix="/rider" )
