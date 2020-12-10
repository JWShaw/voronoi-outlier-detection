import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
import read_data
from sklearn.cluster import KMeans
from sklearn import datasets
from scipy.spatial import Voronoi, voronoi_plot_2d

# Returns the Euclidean distance of two real-valued points	
def euclideanDistance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

# Given an index for a point, returns the indices of the k 
# Voronoi nearest neighbors
def kNearestNeighbors(index, k):
	region = regions[point_region[index]]
	neighbors = []
	for i in range(len(region)):
		sharedEdge = [region[i], region[(i+1) % len(region)]]
		
		for j in range(len(points)):
			if j == index:
				continue
			if all(item in regions[point_region[j]] for item in sharedEdge):
				dist = euclideanDistance(points[index], points[j])
				neighbors.append([j, dist])
				break
	neighbors.sort(key=lambda x: x[1])
	return [neighbor[0] for neighbor in neighbors][:k]

# Returns the k-Distance of a given point.  This is the measure
# of how outlier-like the point is.
def kDistance(index, k):
	sum = 0
	for o in kNearestNeighbors(index, k):
		sum = sum + euclideanDistance(points[index], points[o])
	return sum / k


def genData():
	# Some sample data
	centers_neat = [(-10, 10), (0, -5), (10, 5)]
	x_neat, y_neat = datasets.make_blobs(n_samples=500, 
                                     centers=centers_neat,
                                     cluster_std=2,
                                     random_state=2)

	np.set_printoptions(precision=2)

	# points = np.random.randn(10,2)
	points = x_neat
	return points

"""
Uses read_data.py to gather points for outlier detection
transforms list of points to array
"""
def readData():
	points = np.array(read_data.main())
	return points

"""
Uses matplotlib to generate a scatter plot of data
outliers are shown on a scale from red to blue
red being a point deviating the most from the others
"""
def plot_points(vor,points):
	# Plot results
	k = 3
	voronoi_plot_2d(vor, show_points=False, show_vertices=False, line_width=0.5)
	plot = plt.scatter([item[0] for item in points],
 		[item[1] for item in points],
 		c=[kDistance(i, k) for i in range(len(points))],
		s=3,
 		cmap="coolwarm")

	cbar = plt.colorbar(plot)
	cbar.set_label(f'Voronoi {k}-distance', rotation=270, labelpad=15)

#starting point
if __name__ == "__main__":
	global regions
	points = readData()

	vor = Voronoi(points, furthest_site = False)
	vertices = vor.vertices
	ridge_vertices = vor.regions
	regions = vor.regions
	point_region = vor.point_region

	plot_points(vor,points)
	plt.show()
