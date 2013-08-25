# -*- coding: utf-8 -*-

from models import Piece
from match import Match
from util import maximizeProperty
import ui

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

class Human(Intelligence):

	def selectPiece(self, match):
		return ui.askSelectPiece(match.getUnusedPieces())

	def putOnBoard(self, match, piece):
		return ui.askPosition(match.getUnusedPositions())

class Random(Intelligence):
	"""
	A random intelligence chooses randomly both of location of its current
	piece and the piece to give to its opponent
	"""

	def selectPiece(self, match):
		available_pieces = match.getUnusedPieces()
		i = random.randint(0, len(available_pieces) - 1)

		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		availabe_places = match.getUnusedPositions()
		i = random.randint(0, len(availabe_places) - 1)

		ui.showSelectedPosition(availabe_places[i])

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

	def getNonWiningPieces(self, match, pieces):
		winning_props = match.getWiningProperties()
		list = []
		for p in pieces:
			if not p.color in winning_props \
			and not p.height in winning_props \
			and not p.shape in winning_props \
			and not p.consistency in winning_props:
				list.append(p)
		return list

	def selectPiece(self, match):
		unused_pieces = match.getUnusedPieces()
		available_pieces = self.getNonWiningPieces(match, unused_pieces)
		if len(available_pieces) < 1:
			available_pieces = unused_pieces

		i = random.randint(0, len(available_pieces) - 1)

		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		better_color = maximizeProperty(
			match.board,
			{ "propriety": "color", "value": piece.color }
		)
		better_height = maximizeProperty(
			match.board,
			{ "propriety": "height", "value": piece.height }
		)
		better_shape = maximizeProperty(
			match.board,
			{ "propriety": "shape", "value": piece.shape }
		)
		better_consistency = maximizeProperty(
			match.board,
			{ "propriety": "consistency", "value": piece.consistency }
		)

		val_max = max((
			better_color["value"],
			better_height["value"],
			better_shape["value"],
			better_consistency["value"]
		))

		final_pos = None
		for best in (better_color, better_height, better_shape, better_consistency):
			if best["value"] == val_max:
				final_pos = best["position"]

		if final_pos is None:
			availabe_places = match.getUnusedPositions()
			i = random.randint(0, len(availabe_places) - 1)
			final_pos = availabe_places[i]

		ui.showSelectedPosition(final_pos)

		return final_pos
