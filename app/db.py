from . import app
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy( app )

from .models.account import accounts

security = Security( app, accounts )

def create_default_roles():
	"""
		There are two roles currently. Admin and User.

		The Admin role only allows users marked as an admin to access admin specific
		resources.

		The User role only allows users marked as a user to access user specific
		resources.
	"""

	accounts.create_role( name="Admin", description="This marks a user as a Admin and they can only access the Admin pages and information." )
	accounts.create_role( name="User", description="This marks a user as a User and they can only access the User pages and information." )
	db.session.commit()

db.create_default_roles = create_default_roles
