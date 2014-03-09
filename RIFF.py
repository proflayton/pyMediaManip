'''
Resource Interchange File Format

Will be used as a super class for file formats like AVI
'''

import RIFFChunk

class RIFF:
	chunks = None

	def loadChunks(file):
		temp = file.read(4)
		while temp!=b'':
			chunk = RIFFChunk()
			chunk.identifier = temp
			chunk.length = file.read(4)
			chunk.data = file.read(chunk.length)
			if chunk.length % 2 != 0: #if it is uneven, read in an extra byte
				chunk.pad = file.read(1)
			chunks.append(chunk)
