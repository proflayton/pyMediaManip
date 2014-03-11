'''
Image

'''

from Pixel import Pixel

class Image:
	#Variable Declarations
	pixels      = []
	width 		= 0
	height 		= 0

	#Empty Constructor
	def __init__(self):
		pixels = None

	def __repr__(self):
		return "Image with " + str(len(pixels)) + " pixels"

	def addPixel(self,pixel):
		self.pixels.append(pixel)
	def getPixel(self,x,y):
		if(x >= self.width):
			print("X is out of the height!")
			return None
		elif(y >= self.height):
			print("Y is out of the height!")
			return None
		print(len(self.pixels))
		print(str((y * self.height) + x))
		return self.pixels[(y * self.width) + x]

