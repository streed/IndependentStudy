import sys
import json
import numpy as np

from scipy import spatial

#Read in the data file, for now just out.json, should 
#read in from STDIN to pipe everything together nicely.
data = json.load( open( sys.argv[1] ) )
client_points = json.load( open( sys.argv[2] ) )

steps = data["steps"]

#KDTree expects a numpy.array so convert the points list into
#a numpy.array for use with the KDTree
steps_locs = np.array( [ [ p["loc"]["lat"], p["loc"]["lng"] ] for p in steps ] )

#Build the tree using the GPS coordinates.
tree = spatial.KDTree( steps_locs )

#Begin the finding of the points that are of interest.
for s in client_points:
	loc = np.array( [ s[0], s[1] ] )

	closest = tree.query( loc, k=2, p=2 )
	indexes = closest[1]	
	steps = [ steps[i] for i in indexes ] )
	

