'''
Handle .AVI files
'''
'''
Layout:
RIFF AVI //mandatory
{ RIFF AVIX } //only for Open-DML files
'''

class Chunk:
	#describes type of chunk/list
	#2 hexadecimal digits specifying the stream number
	#2 letters specifying the data type
	#dc = video
	#wb = audio
	#tx = text
	fourCC = None

	#size of the data
	dwSize = None #includes first byte after

	#data
	dwData = None

#fourCC = 'AVI ' is a "RIFF-AVI-List"
#fourCC = 'AVIX' is a "RIFF_AVIX-List"
class List:
	dwList = None
	dwSize = None #includes 4 bytes taken by fourCC
	fourCC = None
	dwData = None

class AVI:
	
	def __init__(self):
		print("Initialize AVI")