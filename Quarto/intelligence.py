# -*- coding: utf-8 -*-

from models import Piece
from match import Match

import random

class Intelligence:
	"""
	Intelligence should be an abstract class.
	It designates, in fact, an artificial intelligence.
	The are different types of AI like Random, Novice or Minimax-D which
	heritated all of Intelligence
	"""

	def selectPiece(self, match):
		pass

	def putOnBoard(self, match, piece):
		pass

class Random(Intelligence):
	"""
	A random intelligence chooses randomly both of location of its current
	piece and the piece to give to its opponent
	"""

	def selectPiece(self, match):
		pieces = match.getUnusedPieces()
		i = random.randint(0, len(pieces) - 1)

		return pieces[i]

	def putOnBoard(self, match, piece):
		availabe_places = match.getUnusedPositions()
		i = random.randint(0, len(availabe_places) - 1)

		return availabe_places[i]
