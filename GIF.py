import binascii
import LZW

'''
Utility Functions
'''
#convert bytes to hex
def bytesToHex(byte):
	return binascii.hexlify(byte)
def bytesToDec(byte):
	return int(binascii.hexlify(byte),16)
#convert hex to dec
def hexToDecimal(hexa):
	return int(hexa,16)
def getBinaryRepresentation(integer):
	try:
		b = lambda x : '%08d' % int(x)
		return b(bin(integer).lstrip('-0b'))
	except:
		return "00000000"#just return empty

class Pixel:
	r = 0
	g = 0
	b = 0
	a = 0

	def __init__(self,r,g,b,a):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def set(self,other):
		self.r = other.r
		self.g = other.g
		self.b = other.b
		self.a = other.a

	def printMe(self):
		print(str(self))

	def __repr__(self):
		return "RGB: (" + str(self.r) + "," + str(self.g) + "," + str(self.b) + ")"

class GIFImage:
	leftPosition= 0
	topPostion 	= 0
	width 		= 0
	height 		= 0
	LCTF		= 0
	interlace	= 0
	sort		= 0
	pixels = []

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

class GIF:
	gifImages = None
	delay = 1 #1ms default

	globalColorTable = [Pixel(0,0,0,255) for x in range(258)]
	localColorTable = [Pixel(0,0,0,255) for x in range(258)]

	def getImage(self,pictureIndex):
		return self.gifImages[pictureIndex]
	def getPixel(self,pictureIndex,x,y):
		return self.gifImages[pictureIndex].getPixel(x,y)
	def setPixel(self,pictureIndex,x,y,pixel):
		self.gifImages[pictureIndex].getPixel(x,y).set(pixel)
	def loadGIF(self,file):
		self.gifImages = []
		print("Loading GIF")
		file.seek(6,0) #skip magic number
		logicalScreenWidth  = file.read(2)
		logicalScreenHeight = file.read(2)
		globalFlags 		= file.read(1)
		globalFlags 		= getBinaryRepresentation(int(binascii.hexlify(globalFlags),16))
		GCTF 				= globalFlags[0]
		globalColorResolution = globalFlags[1:3]
		globalSortFlag		  = globalFlags[4]
		sizeOfGlobalColorTable= globalFlags[5:7]
		sizeOfGlobalColorTable= int(sizeOfGlobalColorTable,2)
		sizeOfGlobalColorTable= 2**(1+sizeOfGlobalColorTable)
		print("GCTF: " + str(GCTF))
		print("Size of Global Table: " + str(sizeOfGlobalColorTable))
		bgColorIndex 		= file.read(1)
		pixelAspectRatio	= file.read(1)

		for i in range(256): #read in the global color table
			r = int(binascii.hexlify(file.read(1)),16)
			g = int(binascii.hexlify(file.read(1)),16)
			b = int(binascii.hexlify(file.read(1)),16)
			self.globalColorTable[i] = Pixel(r,g,b,255)

		tempByte = file.read(1)

		while tempByte != b'\x3B' and tempByte != b'':
			if tempByte == b'\x2C': #imageBlock
				print("")
				gifImage = GIFImage()
				leftPosition= file.read(2)
				topPostion 	= file.read(2)
				width 		= file.read(2)
				height 		= file.read(2)
				flags 		= file.read(1)

				flagBits = getBinaryRepresentation(int(binascii.hexlify(flags),16))
				LCTF = flagBits[0]
				interlace = flagBits[1]
				sort = flagBits[2]
				sizeOfLocalTable = flagBits[4:7]
				sizeOfLocalTable = int(sizeOfLocalTable,2)
				sizeOfLocalTable = 2**(1+sizeOfLocalTable)
				if(LCTF == '0'):
					sizeOfLocalTable = 0

				print("Size of Local Color Table: " + str(sizeOfLocalTable))
				localColorTable = file.read(sizeOfLocalTable)
				LZWMinsize		= file.read(1)
				LZWMinsize	 	= int(binascii.hexlify(LZWMinsize),16) + 1
				blockSize 		= file.read(1)
				blockSize		= int(binascii.hexlify(blockSize),16)

				#Special codes
				clearCode = max(0,min(2**LZWMinsize,256))
				eoiCode = clearCode + 1

				print("Size Of Image Data:" + str(blockSize))
				LZWData = file.read(blockSize)

				print("Bits per data: " + str(LZWMinsize))

				#outFile = open("gifImage.txt","wb")
				#outFile.write(bytes(int(bs,0) for bs in LZWData))
				#outFile.flush()
				#outFile.close()

				#Decompress the imageBlock
				table = self.globalColorTable
				table.append("CLEAR")
				table.append("EOI")
				decompressed = LZW.getTableAndCodesLZWByteStream(LZWData,LZWMinsize,table)
				
				table = decompressed['table']
				codes = decompressed['codes']
				print(codes)
				for x in range(1, len(codes)-1):
					gifImage.addPixel(codes[x])

				realWidth = getBinaryRepresentation(width[1]) + getBinaryRepresentation(width[0])
				realheight = getBinaryRepresentation(height[1]) + getBinaryRepresentation(height[0])
				gifImage.width = int(realWidth,2)
				gifImage.height = int(realheight,2)
				print("GIF [W,H]: ["+str(gifImage.width)+","+str(gifImage.height)+"]")
				self.gifImages.append(gifImage)
				print("Truely at end of Image Block: ",end="")
				print(file.read(1)==b'\x00')
			elif tempByte == b'\x21': #Extension Block
				label = file.read(1)
				if label == b'\xF9': #GCE
					size = file.read(1)
					size = int(binascii.hexlify(size),16)
					flags= file.read(1)
					delay= file.read(2)
					self.delay = int(binascii.hexlify(delay),16) #get the delay in ms
					tci	 = file.read(1) #transparency color index
					print("Truely at end of Extension Block: ",end="")
					print(file.read(1)==b'\x00')
				elif label == b'\xFE': #comment extension block
					size = file.read(1)
					size = int(binascii.hexlify(size),16)
					data = file.read(size)
					print("Truely at end of Extension Block: ",end="")
					print(file.read(1)==b'\x00')
				elif label == '\x01': #Plain Text Extension Block
					size = file.read(1)
					size = int(binascii.hexlify(szie),16)
					textGridLeftPosition = file.read(2)
					textGridTopPosition	 = file.read(2)
					textGridWidth		 = file.read(2)
					textGridHeight		 = file.read(2)
					characterCellWidth	 = file.read(1)
					characterCellHeight	 = file.read(1)
					textForegroundIndex	 = file.read(1)
					textBackgroundIndex	 = file.read(1)
					blockSize			 = file.read(1)
					blockSize = int(binascii.hexlify(blockSize),16)
					data = file.read(blockSize)
					print("Truely at end of Extension Block: ",end="")
					print(file.read(1)==b'\x00')
				elif label == b'\xFF': #Application Extension Block
					size = file.read(1)
					size = int(binascii.hexlify(size),16)
					app	 = file.read(8)
					blockSize = file.read(1)
					blockSize = int(binascii.hexlify(blockSize),16)
					data = file.read(blockSize)
					print("Truely at end of Extension Block: ",end="")
					print(file.read(1)==b'\x00')
			tempByte = file.read(1)
			#print(tempByte)
