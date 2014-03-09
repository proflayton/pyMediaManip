'''
Generic Video Class that will be used in every case after decompression and 
before decompression
'''
import Image

class Video:
	images = None
	audio = None

	def __init__(self):
		images = [Image()]
		audio = Audio()