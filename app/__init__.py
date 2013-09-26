import configparser
import os
from flask import Flask

config = configparser.ConfigParser()
config.readfp( open( os.path.expanduser( "~/.independentStudy" ) ) )

app = Flask( __name__ )

app.debug = config.getboolean( "app", "debug" )
app.config["SQLALCHEMY_DATABASE_URI"] = config.get( "app", "database_uri" )
app.config["SECRET_KEY"] = config.get( "app", "secret_key" )

app.jinja_env.trim_blocks = True
