'''
Pixel


'''

class Pixel:
	red = 0
	green = 0
	blue = 0
	alpha = 0

	def __init__(self,red=0,green=0,blue=0,alpha=255,orig=None):
		if orig!=None:
			self.red   = orig.red
			self.green = orig.green
			self.blue  = orig.blue
			self.alpha = orig.alpha
		else:
			self.red   = red
			self.green = green
			self.blue  = blue
			self.alpha = alpha

	def __repr__(self):
		return "RGBA: ("+str(self.red)+","+str(self.green)+","+str(self.blue)+","+str(self.alpha)+")"