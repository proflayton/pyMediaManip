'''
Utility.py

Holds functions that will be used throughout the library
'''

def flatten(l):
	try:
		for item in l:
			yield from flatten(item)
	except TypeError:
		yield l

def getBinaryRepresentation(binary):
	try:
		b = lambda x : '%08d' % int(x)
		return b(binary.lstrip('-0b'))
	except:
		return "00000000"#just return empty

#convert bytes to hex
def bytesToHex(byte):
	return binascii.hexlify(byte)
def bytesToDec(byte):
	return int(binascii.hexlify(byte),16)
#convert hex to dec
def hexToDecimal(hexa):
	return int(hexa,16)