'''
testimages.py

Jusa test program to test the librarys

Author: Brandon Layton
'''

import tkinter, tkinter.filedialog
from GIF import GIF

root = tkinter.Tk()
root.withdraw()

file_path = tkinter.filedialog.askopenfilename()

f = open(file_path,"rb")

myImage = GIF()
myImage.loadGIF(f)

#for p in myImage.getImage(0).pixels:
#	print(p)

images = myImage.getImages()
_i = 0
#see the image in cmd line
for img in images:
	print("Image #"+str(_i))
	img.showImage()
	_i+=1