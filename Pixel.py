'''
Pixel


'''

class Pixel:
	red = 0
	green = 0
	blue = 0
	alpha = 0

	def __init__(self):
		self.red   = 0
		self.green = 0
		self.blue  = 0
		self.alpha = 0

	def __init__(self,red,green,blue,alpha):
		self.red   = red
		self.green = green
		self.blue  = blue
		self.alpha = alpha

	def __repr__(self):
		return "RGBA: ("+str(self.red)+","+str(self.green)+","+str(self.blue)+","+str(self.alpha)+")"