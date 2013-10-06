from .. import app

from nose import with_setup
from nose.tools import assert_equals
import unittest

class TestMain( unittest.TestCase ):

	def setUp( self ):
		app.config["TESTING"] = True
		self.tests = app.test_client()


	def test_main_page( self ):
		response = self.tests.get( "/" )

		assert_equals( 200, response.status_code  )
	
	def test_about_page( self ):
		response = self.tests.get( "/about" )
		assert_equals( 200, response.status_code )

	def test_registration_page( self ):
		response = self.register( "Sean", "Reed", "555-555-5555" )

		assert_equals( 200, response.status_code )

	def register( self, first, last, phone ):
		return self.tests.post( "/registration", data=dict( 
								firstName=first,
								lastName=last,
								phoneNumber=phone ))
