# -*- coding: utf-8 -*-

class Piece:
	'''
	A piece is represented by:
	* a color (blue or red)
	* a height (tall or short)
	* a shape (square or round)
	* a consistency (hollow or solid)
	* and a position (None if not on the game board)
	'''

	PROPERTIES = [
		["blue", "red"],
		["tall", "short"],
		["square", "round"],
		["hollow", "solid"]
	]

	def __init__(self, properties):
		'''
		Initalizes a Piece
		'''
		self.color = properties['color']
		self.height = properties['height']
		self.shape = properties['shape']
		self.consistency = properties['consistency']

		self.position = None

	def getPropriety(self, name):
		if name == "color":
			return self.color
		elif name == "height":
			return self.height
		elif name == "shape":
			return self.shape
		elif name == "consistency":
			return self.consistency

	def color_int(self):
		if self.color == "blue":
			return 1
		else:
			return -1

	def height_int(self):
		if self.height == "tall":
			return 1
		else:
			return -1

	def shape_int(self):
		if self.shape == "square":
			return 1
		else:
			return -1

	def consistency_int(self):
		if self.consistency == "hollow":
			return 1
		else:
			return -1

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

	def __init__(self, match, name, intelligence):
		self.match = match
		self.name = name
		self.intelligence = intelligence

		self.selectedPiece = None

	def hasSelectedPiece(self):
		return not (self.selectedPiece is None)

	def selectPiece(self):
		return self.intelligence.selectPiece(self.match)

	def putOnBoard(self):
		position = self.intelligence.putOnBoard(
			self.match,
			self.selectedPiece
		)

		if self.match.movePiece(self.selectedPiece, position):
			self.selectedPiece = None

	def hasAI(self):
		return not isinstance(self.intelligence, Human)
