'''
Image

'''

from Pixel import Pixel

class Image:
	#Variable Declarations
	pixels      = []
	width 		= 0
	height 		= 0

	def __init__(self,width,height):
		self.width  = width;
		self.height = height;
		self.pixels = [Pixel(0,0,0,255) for x in range(width*height)]

	def __repr__(self):
		return "Image with " + str(len(pixels)) + " pixels"

	def setPixel(self,x,y,pixel):
		self.pixels[(y*self.width) + x] = pixel
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

