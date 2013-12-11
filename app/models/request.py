from ..db import db

class Request( db.Model ):
  id = db.Column( db.Integer, primary_key=True )  
  is_accepted = db.Column( db.Boolean )
  is_deleted = db.Column( db.Boolean )
  driver_id = db.Column( db.Integer, db.ForeignKey( "driver.id" ) )
  rider_id = db.Column( db.Integer, db.ForeignKey( "rider.id" ) )
  schedule_id = db.Column( db.Integer, db.ForeignKey( "schedule.id" ) )
  loc_id = db.Column( db.Integer, db.ForeignKey( "location.id" ) )

  loc = db.relationship( "Location", backref="requestLocation" )

  def __init__( self, loc, is_accepted=False, is_deleted=False ):
    self.loc = loc
    self.is_accepted = is_accepted
    self.is_deleted = is_deleted
