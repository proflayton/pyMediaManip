'''
GIF.py

Author: Brandon Layton
'''
import binascii
from Pixel import Pixel
from Image import Image
import collections
import Utility
import copy
import struct

class GIFImage(Image):
	delay		= 0
	LCTF		= 0
	interlace	= 0
	sort		= 0
	disposalMethod = 0
	transparencyIndex = 0
	

class GIF:
	transparencyIndex = 0
	transparency = 0
	userInput = 0
	disposalMethod = 0
	repetitions = 0
	imagesAmount = 0
	gifImages = None
	delay = 0 #0ms default

	logicalScreenWidth = 0
	logicalScreenHeight = 0

	globalCodes = None
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
		disposedImage = None

		print("Loading GIF")
		file.seek(6,0) #skip magic number
		self.logicalScreenWidth  = int.from_bytes(file.read(2),byteorder="little")
		self.logicalScreenHeight = int.from_bytes(file.read(2),byteorder="little")
		globalFlags 		= int.from_bytes(file.read(1),byteorder="little")
		#print(globalFlags)
		GCTF 				  = (globalFlags>>7)&1
		globalColorResolution = (globalFlags>>4)&7
		globalSortFlag		  = (globalFlags>>3)&1
		sizeOfGlobalColorTable= globalFlags&7
		print(sizeOfGlobalColorTable)
		sizeOfGlobalColorTable= 2**(1+sizeOfGlobalColorTable)
		print(sizeOfGlobalColorTable)
		print("GCTF: " + str(GCTF))
		print("Size of Global Table: " + str(sizeOfGlobalColorTable))
		bgColorIndex 		= int.from_bytes(file.read(1),byteorder='little')
		pixelAspectRatio	= file.read(1)

		for i in range(sizeOfGlobalColorTable): #read in the global color table
			r = int(binascii.hexlify(file.read(1)),16)
			g = int(binascii.hexlify(file.read(1)),16)
			b = int(binascii.hexlify(file.read(1)),16)
			self.globalColorTable.append(Pixel(red=r,green=g,blue=b,alpha=255))

		disposedImage = GIFImage(width=self.logicalScreenWidth,height=self.logicalScreenHeight);
		disposedImage.fill()

		tempByte = file.read(1)

		while tempByte != b'\x3B' and tempByte != b'':
			if tempByte == b'\x2C': #imageBlock
				print("")
				leftPosition= file.read(2)
				topPosition = file.read(2)
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
				table = copy.deepcopy(self.globalColorTable)
				table.append("CLEAR")
				table.append("EOI")
				raster = self.readRasterData(LZWData,LZWMinsize,table)
				indexStream = raster["indexStream"]
				self.globalCodes = raster["codes"]
				#Little endian
				width 	 	 = int.from_bytes(width,byteorder="little")
				height 	 	 = int.from_bytes(height,byteorder="little")
				leftPosition = int.from_bytes(leftPosition,byteorder="little")
				topPosition  = int.from_bytes(topPosition,byteorder="little")
				print("Position: (%s,%s)"%(leftPosition,topPosition))
				print("Width: %s Height: %s\n"%(width,height))

				if self.imagesAmount > 0:
					gifImage = GIFImage(orig=disposedImage)
				else:
					gifImage = GIFImage(width=self.logicalScreenWidth,height=self.logicalScreenHeight)

				for x in range(0, len(indexStream)):
					#print(indexStream[x], end=" ")
					if indexStream[x] == self.transparencyIndex and self.transparency == 1:
						#if we are using transparency and we are on the index
						pass
					else:
						gifImage.setPixel(leftPosition+x%width,topPosition+int(x/width),self.globalColorTable[indexStream[x]])
				#print("GIF Width: %s\nGIF Height: %s\n"%(gifImage.width,gifImage.height))
				#gifImage.showImage()
				gifImage.delay = self.delay;
				gifImage.disposalMethod = self.disposalMethod
				gifImage.transparencyIndex = self.transparencyIndex
				self.gifImages.append(gifImage)
				self.imagesAmount+=1
				atEnd = file.read(1)==b'\x00'
				print("Truely at end of Image Block: ",end="")
				print(atEnd)

				if self.disposalMethod == 1:
					disposedImage = GIFImage(orig=gifImage)
					print("Saving Image")
				elif self.disposalMethod == 2:
					disposedImage.fill(self.globalColorTable[bgColorIndex])
			elif tempByte == b'\x21': #Extension Block
				label = file.read(1)
				if label == b'\xF9': #GCE
					size  = file.read(1)
					size  = int(binascii.hexlify(size),16)
					packed= file.read(1)
					packed = int.from_bytes(packed,byteorder='little')
					self.transparency 	= packed&1
					self.userInput 		= (packed>>1)&1
					self.disposalMethod = (packed>>2)&7

					print("DISPOSAL METHOD: " + str(self.disposalMethod))

					self.delay = int.from_bytes(file.read(2),byteorder='little')
					#transparency color index
					self.transparencyIndex = int.from_bytes(file.read(1),byteorder='little') 
					print("Truely at end of Graphics Control Extension Block: ",end="")
					print(file.read(1)==b'\x00')
				elif label == b'\xFE': #comment extension block
					size = file.read(1)
					size = int(binascii.hexlify(size),16)
					data = file.read(size)
					print("Truely at end of Comment Extension Block: ",end="")
					print(file.read(1)==b'\x00')
				elif label == '\x01': #Plain Text Extension Block
					size = file.read(1)
					blockSize = int(binascii.hexlify(size),16)
					file.read(blockSize)
					while file.read(1) != b'\x00':
						pass
					print("End of Plain Text Extension Block",end="")
				elif label == b'\xFF': #Application Extension Block
					size = file.read(1)
					size = int(binascii.hexlify(size),16)
					app	 = file.read(size)
					size = file.read(1)
					data = file.read(int(binascii.hexlify(size),16))
					if app == b"NETSCAPE2.0":
						self.repetitions = int.from_bytes(data[1:2],byteorder="little")
						print("reps:" + str(self.repetitions))
					print("Truely at end of Application Extension Block: ",end="")
					print(file.read(1)==b'\x00')
			tempByte = file.read(1)

	#gets the decimal code values from a LZW byte stream
	#pretty much uses the same algorithm as the decompressor
	def readRasterData(self,byteStream,minimumSize,table):
		print(minimumSize)
		#variables for streams
		firstCode = True
		code = None
		prev = []
		indexStream= []
		codes = [] #this will hold all of our code that we don't need after we get indexes

		#Varaibles for reading
		maxIndex = minimumSize
		index = 0
		arrayPos = 0

		#initialize the table
		for i in range(len(table)): #
			if table[i]=="CLEAR":
				print("CLEAR AT " + str(i))
				codes.append(["CLEAR"])
			elif table[i] == "EOI":
				print("EOI AT " + str(i))
				codes.append(["EOI"])
			else:
				codes.append([i])

		#print("Raster Data Table: -BEFORE")
		#print(table)
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
				#print((intVal>>(index%8) & 1),end="")
			#print(" ",end="")
			if not scrap:
				#print(code,end=" ")
				if firstCode:
					if codes[code] != ["CLEAR"]:
						prev = []
						for ele in codes[code]:
							prev.append(ele)
							indexStream.append(ele)
							#print(ele,end=" ") #CLEAR
							firstCode = False
				elif len(codes)-1 < code: #code doesn't exist yet
					#print(str(code) + " does not exist yet")
					k = prev[0]
					temp = []
					for ele in prev:
						temp.append(ele)
					temp.append(k)
					prev = []
					for ele in temp:
						prev.append(ele)
						indexStream.append(ele)
						#print(ele,end=" ")
					codes.append(temp)
				else:
					if codes[code] == ["CLEAR"]: #CLEAR
						continue;
					elif codes[code] == ["EOI"]: #EOI
						#print("EOI when codes was " + str(len(codes)))
						break;
					else:
						#print(str(code), end=", ")
						temp = prev
						k = codes[code][0]
						prev = []
						for ele in codes[code]: #put the indexs into the index stream
							prev.append(ele)
							indexStream.append(ele)
							#print(ele,end=" ")
						temp.append(k) #codes[code-1]+k
						codes.append(temp)

			else: #we are at the end, just scrap bits left
				break;

			if len(codes)-1 >= 2**maxIndex-1:
				print("maxIndex met: ",end="")
				print(maxIndex)
				maxIndex += 1

		#print("Raster Data Table: -AFTER")
		#print(table)
		return {"indexStream":indexStream,"codes":codes}

	def save(self,path):
		if self.gifImages == None:
			print("Load or create an image first!")
			return;
		colors = []
		#some precursor checks, to see if we need to compress
		for image in self.gifImages:
			for pixel in image.getPixels():
				if not pixel.getRGB() in colors:
					print(pixel.getRGB())
					colors.append(pixel.getRGB())
		#have to compress
		if len(colors)>256:
			for image in self.gifImages:
				image.compressLinearly()

		#time to save
		file = open(path,'wb+')
		#write magic number
		file.write(b'\x47\x49\x46\x38\x39\x61')
		file.write(struct.pack('<H',self.logicalScreenWidth))
		file.write(struct.pack('<H',self.logicalScreenHeight))
		closestColorSize = 1
		while 2**(closestColorSize+1) < len(colors):
			closestColorSize += 1
		closestColorSize -= 1
		packed = 0
		packed += closestColorSize
		#ignore sort flag
		packed += 1<<5
		packed += 1<<7
		file.write(struct.pack('<B',packed))
		#time for global color table
		i = 0
		for c in colors:
			file.write(struct.pack('<B',c[0]))
			file.write(struct.pack('<B',c[1]))
			file.write(struct.pack('<B',c[2]))
			i+=1
		#finish it with empty colors
		while i < 2**(closestColorSize+1):
			file.write(b'\x00')
			file.write(b'\x00')
			file.write(b'\x00')
			i+=1

		#if we have animation we have to do netscape2.0 application extension
		if len(self.gifImages) > 1:
			file.write(b'\x21\xFF\x0B')
			file.write(b'NETSCAPE2.0')
			file.write(b'\x03')
			file.write(b'\x01')
			file.write(struct.pack('<H',self.repetitions))
			file.write(b'\x00')
		#time to write image data
		for image in self.gifImages:
			#Graphic Control Extension
			file.write(b'\x21\xF9\x04')
			packed = 0
			packed += self.transparency
			#ignore input flag
			packed += image.disposalMethod << 2
			file.write(struct.pack('<B',packed))
			file.write(struct.pack('<H',image.delay))
			file.write(struct.pack("<B",image.transparencyIndex))
			file.write(b"\x00")

			#image descriptor
			file.write(b"\x2C")
			file.write(struct.pack('<H',0 				  ))
			file.write(struct.pack('<H',0 				  ))
			file.write(struct.pack('<H',image.width 	  ))
			file.write(struct.pack('<H',image.height 	  ))
			packed = 0 #for local table. not handling that at the moment
			file.write(struct.pack('<B',packed))

			#image data
			#LZW DATAAA
			#Start off by creating an indexStream
			indexStream = []
			for pixels in image.getPixels():
				indexStream.append(colors.index(pixels.getRGB()))

			table = copy.deepcopy(colors)
			table.append(0) #CC
			table.append(0) #EOI
			eoi = len(table)-1
			indexBuffer = []
			codeStream 	= []
			codeStream.append(eoi-1) #CC

			i = 0
			k = indexStream[i]
			indexBuffer.append(k)
			i+=1
			while i < len(indexStream):
				k = indexStream[i]
				indexBuffer.append(k)
				temp = indexBuffer
				temp.append(k)
				if temp in table:
					indexBuffer.append(k)
				else:
					table.append(temp)
					for indexes in indexBuffer:
						codeStream.append(indexes)
					indexBuffer = [k]
				i+=1
			for indexes in indexBuffer:
				codeStream.append(indexes)
			codeStream.append(eoi) #EOI

			file.write(struct.pack('<B',closestColorSize+1)) #minimum LZW size

			#compress the codestream
			maxIndex = closestColorSize+1
			index = 0
			codeIndex = 0
			arrayPos = 0
			currentByte = 0
			byteStream = []
			for code in codeStream:
				if code == 2**maxIndex - 1:
					print("maxIndex met: ",end="")
					print(maxIndex)
					maxIndex += 1
				codeIndex = 0
				while codeIndex % maxIndex != 0:
					if index % 8 == 0:
						file.write(struct.pack('<B',currentByte))
						currentByte = 0
					currentByte += ((code>>codeIndex)&1)<<index
					index+=1
					codeIndex+=1




			file.write(b"\x00")

			#END OF FILE! :D
			file.write(b"\x3B")


	def getImages(self):
		return self.gifImages