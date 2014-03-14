'''
ColorCube.py

Used for Color Quantization

Uses Uniform Quantization
Right now its pretty stupid, would like to eventually make weighted clusters

Author: Brandon Layton
'''

import math

class ColorCube:

	division = 0

	#default divisions divy up 256 colors (rounded)
	def __init__(self,colorSize = 255): 
		#A = 256
		#B = Size
		#x = #
		#B^3*x = A^3
		self.division = pow(255**3/colorSize,1/3)
		self.clusters = []
		self.cluster(self.division)

	def cluster(self,divisions):
		for i in range(int(255/self.division)):
			self.clusters.append(int(self.division*i))


	#We can assume everything is divided evenly, so we can just do math
	#and distance formulas
	def getClusterIn(self,color):
		if self.division <= 0:
			print("Error. Division is not valid: " + str(self.divisions))
			return None
		if len(self.clusters) == 0:
			print("Error. No Clusters made")
			return None
		
		newColor = [0,0,0]
		for i in range(3):
			closest = None
			closestDistance = None
			for c in self.clusters:
				if closestDistance == None or abs(color[i]-c)<closestDistance:
					closest = c
					closestDistance = abs(color[i]-c)
			newColor[i] = closest

		return newColor
