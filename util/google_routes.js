var util = require( "util" )
var g = require( "googlemaps" )

var polylineParse = function( line ) {
	var points = [];
	var i = 0, lat = 0, lng = 0, point_id = 0;
	while( i < line.length ) {
		var b, shift = 0; result = 0;

		do {
			b = line.charCodeAt( i++ ) - 63;
			result |= ( b & 0x1f ) << shift;
			shift += 5;
		}while( b >= 0x20 );

		var dlat = ( ( result & 1 ) != 0 ? ~( result >> 1 ) : ( result >> 1 ) );
		lat += dlat;

		shift = 0;
		result = 0;	
		do {
			b = line.charCodeAt( i++ ) - 63;
			result |= ( b & 0x1f ) << shift;
			shift += 5;
		}while( b >= 0x20 );

		var dlng = ( ( result & 1 ) != 0 ? ~( result >> 1 ) : ( result >> 1 ) );
		lng += dlng;

		points.push( { lat: lat / 1E5, lng: lng / 1E5, id: point_id } );
		point_id++;
	}

	return points;
}

var parseManeuver = function( instr ) {
	var regex = /([\w]+)[^<]*<b>([^<]+)<\/b>/;
	var result = instr.match( regex );
	return result[1].toLowerCase() + "-" + result[2].toLowerCase();
}

var stepsFilter = function( steps ) {
	var results = [];
	for( var i in steps ) {
		var s =  steps[i];

		//Wrose case we need to parse out the manuever
		//by hand rather than getting told by Google.
		if( s.maneuver === undefined ) {
			s.maneuver = parseManeuver( s.html_instructions );
		}

		//Steps with just a "head" in them does not give 
		//enough information onto the nature of the 
		//direction from our point of view. This is because
		//it does not provide context into whether there
		//is a turn or not at this point, and it is
		//typically one of the first route steps.
		if( s.maneuver.indexOf( "head" ) == -1 ) {
			results.push( { loc: s.start_location, maneuver: s.maneuver } );
		}
	}

	return results;
}

var getDirections = function( route_stack, index, current ) {
	if( current == undefined ) {
		current = { routes: [] };
	}
	if( index == undefined ) {
		index = 0;
	} else if( index >= route_stack.length ) {
		util.puts( JSON.stringify( current ) );
		return;
	}

	cur = route_stack[index].split( " " )

	var slat = cur[0];
	var slng = cur[1];
	var dlat = cur[2];
	var dlng = cur[3];

	var start = slat + " " + slng;
	var end = dlat + " " + dlng;

	g.directions( start, end, function(err, data) {
		if( data ) {
			var r = data.routes;
			//var polyline = r[0].overview_polyline.points;
			//var points = polylineParse( polyline );

			var steps = stepsFilter( r[0].legs[0].steps );

			current.routes.push( { gps: route_stack[index], steps: steps } );

		 	getDirections( route_stack, index + 1, current );
		}
	});

}


//./google_routes.js "37.297923 -80.055787 37.30403 -79.964281"
var args = process.argv.slice( 2 );

getDirections( args );
