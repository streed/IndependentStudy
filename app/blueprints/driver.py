from flask import Blueprint, render_template, abort

driver = Blueprint( "driver", __name__, template_folder="templates" )

@driver.route( "/" )
def index():
	return render_template( "driver/index.html" )

