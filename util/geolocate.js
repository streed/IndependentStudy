var util = require( "util" )
var g = require( "googlemaps" )

var geoLocate = function( args ) {
	g.geocode( args[0], function( err, data ) {
		util.puts( JSON.stringify( data.results[0].geometry.location ) );
	});
};

var args = process.argv.slice( 2 );

geoLocate( args );
