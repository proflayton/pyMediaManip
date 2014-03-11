import binascii
import LZW
from Pixel import Pixel
from Image import Image
import collections
import Utility

class GIFImage(Image):
	leftPosition= 0
	topPostion 	= 0
	LCTF		= 0
	interlace	= 0
	sort		= 0
	

class GIF:
	gifImages = None
	delay = 0 #0ms default

	globalColorTable = []
	localColorTable = []

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
		globalFlags 		= int.from_bytes(file.read(1),byteorder="little")
		#print(globalFlags)
		GCTF 				= globalFlags&128
		globalColorResolution = globalFlags&112
		globalSortFlag		  = globalFlags&8
		sizeOfGlobalColorTable= globalFlags&7
		print(sizeOfGlobalColorTable)
		sizeOfGlobalColorTable= 2**(1+sizeOfGlobalColorTable)
		print(sizeOfGlobalColorTable)
		print("GCTF: " + str(GCTF))
		print("Size of Global Table: " + str(sizeOfGlobalColorTable))
		bgColorIndex 		= file.read(1)
		pixelAspectRatio	= file.read(1)

		for i in range(sizeOfGlobalColorTable): #read in the global color table
			r = int(binascii.hexlify(file.read(1)),16)
			g = int(binascii.hexlify(file.read(1)),16)
			b = int(binascii.hexlify(file.read(1)),16)
			self.globalColorTable.append(Pixel(r,g,b,255))

		tempByte = file.read(1)

		while tempByte != b'\x3B' and tempByte != b'':
			if tempByte == b'\x2C': #imageBlock
				print("")
				leftPosition= file.read(2)
				topPostion 	= file.read(2)
				width 		= file.read(2)
				height 		= file.read(2)
				flags 		= file.read(1)

				flagBits = Utility.getBinaryRepresentation(int(binascii.hexlify(flags),16))
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

				

				print("Size Of Image Data:" + str(blockSize))
				LZWData = file.read(blockSize)

				print("Bits per data: " + str(LZWMinsize))

				#Decompress the imageBlock
				table = self.globalColorTable
				table.append("CLEAR")
				table.append("EOI")
				#Special codes
				eoiCode = len(table)
				clearCode = eoiCode-1
				decompressed = self.readRasterData(LZWData,LZWMinsize,table)
				
				table = decompressed['table']
				codes = decompressed['codes']

				#Little endian
				width 	 	 = int.from_bytes(width,byteorder="little")
				height 	 = int.from_bytes(height,byteorder="little")
				leftPosition= int.from_bytes(leftPosition,byteorder="little")
				topPostion  = int.from_bytes(topPostion,byteorder="little")

				gifImage = GIFImage(width,height)
				gifImage.leftPosition = leftPosition
				gifImage.topPostion = topPostion

				for x in range(1, len(codes)-1):
					#print(codes[x])
					gifImage.setPixel(x%gifImage.width,int(x/gifImage.width),codes[x])

				print("Width: %s\nHeight: %s\n"%(gifImage.width,gifImage.height))

				self.gifImages.append(gifImage)
				atEnd = file.read(1)==b'\x00'
				print("Truely at end of Image Block: ",end="")
				print(atEnd)
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

	#gets the decimal code values from a LZW byte stream
	#pretty much uses the same algorithm as the decompressor
	def readRasterData(self,byteStream,minimumSize,table):
		maxIndex = minimumSize
		codes = []
		temp = None
		tempCode = ''
		index = 0
		arrayPos = 0
		for i in range(len(table)):
			table[i] = [table[i]]
		print("Raster Data Table: -BEFORE")
		print(table)
		while arrayPos < len(byteStream):
			mult = 1
			bitsRead = 0
			code = 0
			scrap = False
			while bitsRead < maxIndex:
				if arrayPos >= len(byteStream):
					scrap = True
					break;
				intVal = byteStream[arrayPos]
				code += mult*(intVal>>(index%8) & 1)
				index+=1
				arrayPos=int(index/8)
				mult = 2**(1+bitsRead)
				bitsRead+=1
			if not scrap:
				print(code,end=" ")
				if table[code]=='TEMP': #GIF handling
					print("Just a clear or end of data")
					#for c in Utility.flatten(table[code]):
						#codes.append(c)
				elif table[code] == 'EOI':
					print("EOI")
					break;
				else:
					try:
						if table[code] != None:
							if temp != None:
								tempArray = []
								for i in table[temp]:
									tempArray.append(i)
								tempArray.append(table[code][0])
								table.append(tempArray)
								for c in table[code]:
									codes.append(c)
							else:
								for c in table[code]:
									codes.append(c)
					except:
						if temp != None:
							tempArray = []
							for i in table[temp]:
								tempArray.append(i)
							tempArray.append(table[temp][0])
							table.append(tempArray)
							for c in table[code]:
								codes.append(c)
				temp = code
			else:
				break;
			if code >= 2**maxIndex-1:
				print("maxIndex met: ",end="")
				print(maxIndex)
				maxIndex += 1

		print("Raster Data Table: -AFTER")
		#print(table)
		return {"codes":codes,"table":table}

	def saveGIF(self,path):
		if gifImages == None:
			print("Load or create an image first!")
			return;
		
	def showImage(self,imgIndex):
		x = 0
		y = 0
		for pixel in self.gifImages[imgIndex].pixels:
			avg = (pixel.red + pixel.green + pixel.blue)/3
			#print(pixel)
			if avg > 170:
				s1 = '= '
			elif avg > 85:
				s1 = '+ '
			else:
				s1 = '- '
			print(s1,end="")
			x+=1
			if x % self.gifImages[imgIndex].width == 0:
				print("")
				x = 0
				y += 1