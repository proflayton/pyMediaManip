import tkinter, tkinter.filedialog
import GIF
from GIF import GIF
from GIF import Pixel

root = tkinter.Tk()
root.withdraw()

file_path = tkinter.filedialog.askopenfilename()

f = open(file_path,"rb")

myImage = GIF()
myImage.loadGIF(f)

for p in myImage.getImage(0).pixels:
	print(p)

running = True
print("type -1 to quit")
while running:
	x = int(input('What is the x position of the Pixel you want?'))
	if(x == -1):
		break
	y = int(input('What is the y position of the Pixel you want?'))
	if(y == -1):
		break
	pixel = myImage.getPixel(0,x,y)
	if(pixel == None):
		print("Pixel doesn't exist there")
	else:
		pixel.printMe()
	print("type -1 to not set color")
	r = int(input('What is the red of that pixel?'))
	if r == -1: continue
	g = int(input('What is the green of that pixel?'))
	if g == -1: continue
	b = int(input('What is the blue of that pixel?'))
	if b == -1: continue
	myImage.setPixel(0,x,y,Pixel(r,g,b,255))
	print("--------------")