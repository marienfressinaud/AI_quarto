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
		available_pieces = match.getUnusedPieces()
		i = random.randint(0, len(available_pieces) - 1)

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		availabe_places = match.getUnusedPositions()
		i = random.randint(0, len(availabe_places) - 1)

		return availabe_places[i]

class Novice(Intelligence):
	"""
	A novice intelligence plays as follows:
	* It always places its piece in a winning formation, if possible.
	  Otherwise, it chooses randomly among the existing open cells.
	* If given a choice among pieces to give the opponent, it always chooses
	  one that cannot be used to immediately win the game,
	  if such a piece is available.
	"""

	def getNonWiningPiece(self, match, pieces):
		# TODO
		pass

	def selectPiece(self, match):
		unused_pieces = match.getUnusedPieces()
		piece = self.getNonWiningPiece(match, unused_pieces)
		if piece is None:
			i = random.randint(0, len(unused_pieces) - 1)
			piece = unused_pieces[i]

		return piece