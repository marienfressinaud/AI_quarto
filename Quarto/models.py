# -*- coding: utf-8 -*-

from util import get_board_values

class Piece:
	'''
	A piece is represented by:
	* a color (blue or red)
	* a height (tall or short)
	* a shape (square or round)
	* a state (hollow or solid)
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
		self.state = properties['state']

		self.position = None

	def getPropriety(self, name):
		if name == "color":
			return self.color
		elif name == "height":
			return self.height
		elif name == "shape":
			return self.shape
		elif name == "state":
			return self.state

	def __equal1(self, prop, value):
		if prop == value:
			return 1
		return -1

	def color_int(self):
		return self.__equal1(self.color, "blue")

	def height_int(self):
		return self.__equal1(self.height, "tall")

	def shape_int(self):
		return self.__equal1(self.shape, "square")

	def state_int(self):
		return self.__equal1(self.state, "hollow")

	def __str__(self):
		image = ""
		if self.color == "blue":
			image = "b"
		else:
			image = "r"

		if self.height == "tall":
			image = image.upper()

		if self.state == "hollow":
			image = image + "*"

		if self.shape == "round":
			image = "(" + image + ")"

		return image

	def str_server_style(self):
		image = ""
		if self.color == "blue":
			image = "B"
		else:
			image = "R"

		if self.height == "tall":
			image += "L"
		else:
			image += "S"

		if self.shape == "round":
			image += "C"
		else:
			image += "S"

		if self.state == "hollow":
			image += "H"
		else:
			image += "N"

		return image

class Board:
	'''
	A board is where we put pieces.
	It will be manipulate by Minimax Intelligence so it should be no heavy
	'''

	MAX_BOARD_ROWS = 4
	MAX_BOARD_COLS = 4

	def initPieces(self):
		self.pieces = []

		for i in xrange(16):
			color = Piece.PROPERTIES[0][i / 8 % 2]
			height = Piece.PROPERTIES[1][i / 4 % 2]
			shape = Piece.PROPERTIES[2][i / 2 % 2]
			state = Piece.PROPERTIES[3][i % 2]

			piece = Piece({
				"color": color,
				"height": height,
				"shape": shape,
				"state": state
			})

			self.pieces.append(piece)

	def __init__(self):
		self.initPieces()

		cols = self.MAX_BOARD_COLS
		rows = self.MAX_BOARD_ROWS
		self.board = [[None for j in xrange(cols)] for i in xrange(rows)]

	def unusedPieces(self):
		list = []

		for piece in self.pieces:
			if piece.position is None:
				list.append(piece)

		return list

	def unusedPositions(self):
		list = []

		for i in xrange(self.MAX_BOARD_ROWS):
			for j in xrange(self.MAX_BOARD_COLS):
				if self.board[i][j] is None:
					list.append({
						"x": i,
						"y": j
					})

		return list

	def getPiece(self, image_piece):
		for piece in self.unusedPieces():
			if image_piece == str(piece):
				return piece

		return None

	def putPiece(self, piece, pos):
		if self.board[pos["x"]][pos["y"]] is None:
			self.board[pos["x"]][pos["y"]] = piece
			piece.position = pos
			return True
		return False

	def takeOff(self, piece):
		pos = piece.position

		if not (pos is None):
			self.board[pos["x"]][pos["y"]] = None
			piece.position = None

	def isFull(self):
		return len(self.unusedPositions()) == 0

	def isWon(self):
		for board_values in get_board_values(self.board):
			color = board_values["color"] ** 2
			height = board_values["height"] ** 2
			shape = board_values["shape"] ** 2
			state = board_values["state"] ** 2

			if color == 16 or height == 16 \
			or shape == 16 or state == 16:
				return True

		return False

	def __str__(self):
		image = "  "
		for j in xrange(len(self.board[0])):
			image += "%3d   " % (j + 1)
		image += "\n" + ("-" * 26) + "\n"

		for i in xrange(len(self.board)):
			image += str(i + 1) + "|"
			for j in xrange(len(self.board[0])):
				piece = self.board[i][j]
				if piece is None:
					image += "%5s|" % ""
				else:
					image += "%4s |" % str(piece)
			image += "\n"

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

		if self.match.board.putPiece(self.selectedPiece, position):
			self.selectedPiece = None

	def hasAI(self):
		return not isinstance(self.intelligence, Human)
