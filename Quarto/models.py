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

class Board:
	'''
	A board is where we put pieces.
	It will be manipulate by Minimax Intelligence so it should be no heavy
	'''

	MAX_BOARD_ROWS = 4
	MAX_BOARD_COLS = 4

	def initPieces(self):
		self.pieces = []

		for i in range(16):
			color = Piece.PROPERTIES[0][i / 8 % 2]
			height = Piece.PROPERTIES[1][i / 4 % 2]
			shape = Piece.PROPERTIES[2][i / 2 % 2]
			consistency = Piece.PROPERTIES[3][i % 2]

			piece = Piece({
				"color": color,
				"height": height,
				"shape": shape,
				"consistency": consistency
			})

			self.pieces.append(piece)

	def __init__(self):
		self.initPieces()

		cols = self.MAX_BOARD_COLS
		rows = self.MAX_BOARD_ROWS
		self.board = [[None for j in range(cols)] for i in range(rows)]

	def unusedPieces(self):
		list = []

		for piece in self.pieces:
			if piece.position is None:
				list.append(piece)

		return list

	def unusedPositions(self):
		list = []

		for i in range(self.MAX_BOARD_ROWS):
			for j in range(self.MAX_BOARD_COLS):
				if self.board[i][j] is None:
					list.append({
						"x": i,
						"y": j
					})

		return list

	def movePiece(self, piece, pos):
		if self.board[pos["x"]][pos["y"]] is None:
			self.board[pos["x"]][pos["y"]] = piece
			piece.position = pos
			return True
		return False

	def isFull(self):
		return len(self.unusedPositions()) == 0

	def __str__(self):
		image = "  "
		for j in range(len(self.board[0])):
			image += "%3d   " % (j + 1)
		image += "\n" + ("-" * 30) + "\n"

		for i in range(len(self.board)):
			image += str(i + 1) + "|"
			for j in range(len(self.board[0])):
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

		if self.match.board.movePiece(self.selectedPiece, position):
			self.selectedPiece = None

	def hasAI(self):
		return not isinstance(self.intelligence, Human)
