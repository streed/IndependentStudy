import sys
import json
import numpy as np

from scipy import spatial

#Read in the data file, for now just out.json, should 
#read in from STDIN to pipe everything together nicely.
data = json.load( open( sys.argv[1] ) )
client_points = json.load( open( sys.argv[2] ) )

routes = data["routes"]

#KDTree expects a numpy.array so convert the points list into
#a numpy.array for use with the KDTree
route_ids = []
route_id = 0
steps_locs = []
for steps in routes:
	route_ids += [ route_id ] * len( steps["steps"] )
	steps_locs += [ [ p["loc"]["lat"], p["loc"]["lng"] ] for p in steps["steps"] ]

	route_id += 1

steps_locs = np.array( steps_locs )

print( "Number of steps:", len( steps_locs ) )

#Build the tree using the GPS coordinates.
tree = spatial.cKDTree( steps_locs )

#Begin the finding of the points that are of interest.
steps = {}
for s in client_points:
	loc = np.array( [ s[0], s[1] ] )

	closest = tree.query( loc, k=2 )
	indexes = closest[1]	
	steps["%f %f" % ( s[0], s[1] )] = list( set( [ routes[route_ids[i]]["gps"] for i in indexes ] ) )

print( steps )
