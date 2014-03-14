'''
Image.py

Author: Brandon Layton

'''

from Pixel import Pixel
import Utility
import math
from ColorCube import ColorCube

class Image:
	#Variable Declarations
	pixels      = []
	width 		= 0
	height 		= 0

	def __init__(self,width=0,height=0,orig=None):
		if orig == None:
			self.width  = width;
			self.height = height;
			self.pixels = [Pixel(0,0,0,255) for x in range(width*height)]
		else:
			self.width = orig.width
			self.height = orig.height
			self.pixels = [Pixel(0,0,0,255) for x in range(self.width*self.height)]
			for i in range(self.width * self.height):
				self.pixels[i] = Pixel(orig=orig.pixels[i])

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
	def getPixels(self):
		return self.pixels

	def fill(self,pixel=Pixel()):
		for i in range(len(self.pixels)):
			self.pixels[i] = pixel

	#Color Quantization
	#this is really bad at the moment
	def compress(self,numberOfColors=256):
		colorCube = ColorCube(numberOfColors)
		for p1 in self.pixels:
			color = colorCube.getClusterIn(p1.getRGB())
			print(p1.getRGB(),end="")
			print("->",end="")
			print(color)

	#just rounds the colors in 50's increments
	#6**3 is less than 256, so this can be made into a GIF
	def compressLinear(self):
		for p1 in self.pixels:
			color = p1.getRGB()
			newColor = [0,0,0]
			clusters = [0,50,100,150,200,250]
			for i in range(3):
				closest = None
				closestDistance = None
				for c in clusters:
					if closestDistance == None or abs(color[i]-c)<closestDistance:
						closest = c
						closestDistance = abs(color[i]-c)
				newColor[i] = closest
			p1.setRGB(newColor)
			print(p1)

		return newColor
			



	#Print the image into command line arbitrarily 
	#(Red Green Blue Yellow Black White)
	#Finds the closest the pixel is to and uses that as the "color"
	def showImage(self):
		x = 0
		y = 0
		yellow= Pixel(red=255,blue=255,green=0  ,alpha=255)
		red   = Pixel(red=255,blue=0  ,green=0  ,alpha=255)
		green = Pixel(red=0  ,blue=0  ,green=255,alpha=255)
		blue  = Pixel(red=0  ,blue=255,green=0  ,alpha=255)
		black = Pixel(red=0  ,blue=0  ,green=0  ,alpha=255)
		white = Pixel(red=255,blue=255,green=255,alpha=255)
		for pixel in self.pixels:
			#print(pixel)
			yD = [Utility.colorDistance(yellow,pixel),'y ']
			rD = [Utility.colorDistance(red,pixel)   ,'r ']
			gD = [Utility.colorDistance(green,pixel) ,'g ']
			bD = [Utility.colorDistance(blue,pixel)  ,'b ']
			bkD= [Utility.colorDistance(black,pixel) ,'B ']
			wD = [Utility.colorDistance(white,pixel) ,'w ']
			distances = [yD,rD,gD,bD,bkD,wD]
			closest = distances[0]
			for i in range(1,len(distances)):
				if distances[i][0] < closest[0]:
					closest = distances[i]

			print(closest[1],end="")
			x+=1
			if x % self.width == 0:
				print("")
				x = 0
				y += 1