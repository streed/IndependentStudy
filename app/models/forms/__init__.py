from flask_wtf import Form
from flask_wtf.html5 import EmailField, TelField, IntegerField
from wtforms import TextField, IntegerField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class AccountForm( Form ):
	email = EmailField( "Email", validators=[DataRequired()] )
	password = PasswordField( "Password", validators=[DataRequired()] )
	name = TextField( "Name", validators=[DataRequired()] )
	age = IntegerField( "Age", validators=[DataRequired()] )
	phoneNumber = TelField( "Phone Number", validators=[DataRequired()] )

class LoginForm( Form ):
	email = EmailField( "Email", validators=[DataRequired()] )
	password = TextField( "Password", validators=[DataRequired()] )

