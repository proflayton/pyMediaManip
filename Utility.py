'''
Utility.py

Holds functions that will be used throughout the library
'''

import collections
import binascii
import math

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el

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
	print(byte)
	return int(byte,16)
#convert hex to dec
def hexToDecimal(hexa):
	return int(hexa,16)

def colorDistance(c1,c2):
	return abs(c1.red - c2.red) + abs(c1.blue - c2.blue) + abs(c1.green - c2.green)