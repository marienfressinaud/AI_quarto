# -*- coding: utf-8 -*-

class Piece:
	'''
	A piece is represented by:
	* a color (blue or red)
	* a height (tall or short)
	* a shape (square or round)
	* a consistency (hollow or solid)
	'''

	def __init__(self, properties):
		'''
		Initalizes a Piece
		'''
		self.color = properties['color']
		self.height = properties['height']
		self.shape = properties['shape']
		self.consistency = properties['consistency']

	def __str__(self):
		image = ""
		if self.color == "blue":
			image = "b"
		else:
			image = "r"

		if self.height == "tall":
			image = image.upper()

		if self.consistency == "hollow":
			image = image + "*"

		if self.shape == "round":
			image = "(" + image + ")"

		return image


class Player:
	'''
	A Player is defined by:
	* a name
	* an intelligence (AI or not)
	'''

	def __init__(self, name, intelligence):
		self.name = name
		self.intelligence = intelligence

		if(self.intelligence is None):
			self.isAI = False
		else:
			self.isAI = True

	def selectPiece():
		print "Not yet implemented"
		return None

	def putOnBoard():
		print "Not yet implemented"
		return None
