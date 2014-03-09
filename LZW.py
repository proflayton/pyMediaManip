'''
Created by Brandon Layton
Last Updated: 2/25/2014

Created to handle LZW bytestreams
'''
import binascii
import math
import collections
import Utility

def decompressLZWByteStream(byteStream,minimumSize,table):
	maxIndex = minimumSize
	#print(maxIndex)
	decompressed = []
	i = minimumSize
	index = 0;
	arrayPos = 0;
	tmp = ""
	while(arrayPos < len(byteStream)):
		mult = 1;
		bitsRead = 0;
		code = 0
		scrap = False #did we run out of bits early?
		while bitsRead < maxIndex:
			if arrayPos >= len(byteStream):
				scrap = True
				break
			intVal = byteStream[arrayPos]
			#		(2**n)*the bit we are on
			code += mult*((intVal>>(index%8))&1) #grabs least significant bit after shifting index amount
			#print((intVal>>(index%8))&1)
			index += 1
			arrayPos = int(index / 8)
			mult = 2**(1+bitsRead)
			bitsRead += 1
		if len(tmp) == 0:#first time
			tmp.append(code)
		#print(code)
		#decompressed.append(code)
		if scrap:
			print("hit scrap")
			break
		elif table.get(code,-1) == -1:
			tmp.append(tmp[0])
			table[code] = tmp
			print(table)
		else:
			print(table[code])
			if len(bin(code)) - 2 > maxIndex + 1: #-2 because of the 0b prefix
				maxIndex += 1 #variable length
				#do something
			phrase = tmp + tmp[0]
			print(phrase)
			table[code] = phrase
		if code >= 2**maxIndex - 1:
			print("maxIndex met: ",end="")
			print(maxIndex)
			maxIndex += 1

#gets the decimal code values from a LZW byte stream
#pretty much uses the same algorithm as the decompressor
def getTableAndCodesLZWByteStream(byteStream,minimumSize,table):
	maxIndex = minimumSize
	codes = []
	temp = None
	tempCode = ''
	index = 0
	arrayPos = 0
	#Initialize the table with atleast 1 array
	for i in range(len(table)):
		if type(table[i]) is not collections.Iterable:
			table[i] = [table[i]]
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
			if code == minimumSize or code == minimumSize + 1: #GIF handling
				print("Just a clear or end of data")
				for c in flatten(table[code]):
					codes.append(c)
			else:
				try:
					if table[code] != None:
						if temp != None:
							tempArray = [
								flatten(table[temp]),
								table[code][0]
								]
							table.append(tempArray)
							for c in flatten(table[code]):
								codes.append(c)
						else:
							for c in flatten(table[code]):
								codes.append(c)
				except:
					if temp != None:
						tempArray = [
							flatten(table[temp]),
							table[temp][0]
							]
						table.append(tempArray)
						for c in flatten(table[code]):
							codes.append(c)
						print(temp,end=" ")
				temp = code
		else:
			break;
		if code >= 2**maxIndex -1:
			#print("maxIndex met: ",end="")
			#print(maxIndex)
			maxIndex += 1
	return {"codes":codes,"table":table}
