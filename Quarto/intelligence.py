# -*- coding: utf-8 -*-

import random

from models import Piece
from match import Match
from util import maximize_property, eval_position, get_wining_properties, \
	get_board_values
import ui

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
		ui.showPlayer(match.active_player)
		return ui.askSelectPiece(match.board.unusedPieces())

	def putOnBoard(self, match, piece):
		ui.showPlayer(match.active_player)
		return ui.askPosition(match.board.unusedPositions())

class Random(Intelligence):
	"""
	A random intelligence chooses randomly both of location of its current
	piece and the piece to give to its opponent
	"""

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		if len(available_pieces) < 1:
			# trick for tournament, when board is full
			return Piece({
				"color": "blue",
				"height": "small",
				"shape": "round",
				"state": "solid"
			})

		i = random.randint(0, len(available_pieces) - 1)

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()
		i = random.randint(0, len(available_pos) - 1)

		ui.showPlayer(match.active_player)
		ui.showSelectedPosition(available_pos[i])

		return available_pos[i]

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
		winning_props = get_wining_properties(match.board.board)
		list = []
		for p in pieces:
			if not p.color in winning_props \
			and not p.height in winning_props \
			and not p.shape in winning_props \
			and not p.state in winning_props:
				list.append(p)
		return list

	def selectPiece(self, match):
		unused_pieces = match.board.unusedPieces()
		if len(unused_pieces) < 1:
			# trick for tournament, when board is full
			return Piece({
				"color": "blue",
				"height": "small",
				"shape": "round",
				"state": "solid"
			})

		available_pieces = self.getNonWiningPieces(match, unused_pieces)
		if len(available_pieces) < 1:
			available_pieces = unused_pieces

		if len(available_pieces) >= 15:
			return Random().selectPiece(match)

		i = random.randint(0, len(available_pieces) - 1)

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()

		if len(available_pos) >= 15:
			return Random().putOnBoard(match, piece)

		board_values = get_board_values(match.board.board)
		better_color = maximize_property(
			match.board.board,
			{ "propriety": "color", "value": piece.color },
			board_values
		)
		better_height = maximize_property(
			match.board.board,
			{ "propriety": "height", "value": piece.height },
			board_values
		)
		better_shape = maximize_property(
			match.board.board,
			{ "propriety": "shape", "value": piece.shape },
			board_values
		)
		better_state = maximize_property(
			match.board.board,
			{ "propriety": "state", "value": piece.state },
			board_values
		)

		val_max = max((
			better_color["value"],
			better_height["value"],
			better_shape["value"],
			better_state["value"]
		))

		final_pos = None
		for best in (better_color, better_height, \
		             better_shape, better_state):
			if best["value"] == val_max:
				final_pos = best["position"]

		if final_pos is None:
			i = random.randint(0, len(available_pos) - 1)
			final_pos = available_pos[i]

		ui.showPlayer(match.active_player)
		ui.showSelectedPosition(final_pos)

		return final_pos

class Minimax(Intelligence):
	"""
	A Minimax intelligence implements Minimax algorithm
	with alpha-beta pruning. It must be the better player!
	"""

	MINIMAX_1_UNTIL = 12
	MINIMAX_2_UNTIL = 10
	MINIMAX_3_UNTIL = 8

	MAX_VAL_DEPTH = 4

	STATE_MAX = 1
	STATE_MIN = 2

	EVAL_WIN = 500
	EVAL_DRAW = 490

	def __init__(self, depth):
		if depth < 1:
			depth = 1
		elif depth > Minimax.MAX_VAL_DEPTH:
			depth = Minimax.MAX_VAL_DEPTH

		self.max_depth = depth

	def evaluation(self, board, played_pos, state):
		eval_pos = 0

		if board.isWon():
			eval_pos = Minimax.EVAL_WIN
		elif board.isFull():
			eval_pos = Minimax.EVAL_DRAW
		else:
			eval_pos = min(
				Minimax.EVAL_WIN - 20, eval_position(board.board, played_pos)
			)

		final_eval = eval_pos
		if state == Minimax.STATE_MAX:
			final_eval = Minimax.EVAL_WIN - final_eval

		return final_eval

	def max_evaluation(self, board, played_piece, played_pos,
		               alpha, beta, depth):
		board.putPiece(played_piece, played_pos)

		available_pieces = board.unusedPieces()
		available_pos = board.unusedPositions()
		best_eval = 0

		if board.isWon() or board.isFull() or depth >= self.max_depth:
			best_eval = self.evaluation(board, played_pos, Minimax.STATE_MAX)
		else:
			for piece in available_pieces:
				for pos in available_pos:
					best_eval = max(best_eval,
						self.min_evaluation(
							board, piece, pos,
							alpha, beta, depth + 1
						)
					)

					if best_eval >= beta:
						board.takeOff(played_piece)
						return best_eval

					alpha = max(alpha, best_eval)

		board.takeOff(played_piece)
		return best_eval

	def min_evaluation(self, board, played_piece, played_pos,
		               alpha, beta, depth):
		board.putPiece(played_piece, played_pos)

		available_pieces = board.unusedPieces()
		available_pos = board.unusedPositions()
		best_eval = Minimax.EVAL_WIN

		if board.isWon() or board.isFull() or depth >= self.max_depth:
			best_eval = self.evaluation(board, played_pos, Minimax.STATE_MIN)
		else:
			for piece in available_pieces:
				for pos in available_pos:
					best_eval = min(best_eval,
						self.max_evaluation(
							board, piece, pos,
							alpha, beta, depth + 1
						)
					)

					if alpha >= best_eval:
						board.takeOff(played_piece)
						return best_eval

					beta = min(beta, best_eval)

		board.takeOff(played_piece)
		return best_eval

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		if len(available_pieces) < 1:
			# trick for tournament, when board is full
			return Piece({
				"color": "blue", "height": "small",
				"shape": "round", "state": "solid"
			})

		available_pos = match.board.unusedPositions()
		fallback_i = random.randint(0, len(available_pieces) - 1)
		chosen_piece = available_pieces[fallback_i]
		alpha, beta = 0, Minimax.EVAL_WIN

		if len(available_pieces) >= Minimax.MINIMAX_1_UNTIL and \
				self.max_depth > 1:
			return Minimax(1).selectPiece(match)
		if len(available_pieces) >= Minimax.MINIMAX_2_UNTIL and \
				self.max_depth > 2:
			return Minimax(2).selectPiece(match)
		if len(available_pieces) >= Minimax.MINIMAX_3_UNTIL and \
				self.max_depth > 3:
			return Minimax(3).selectPiece(match)

		for piece in available_pieces:
			alpha = 0

			for pos in available_pos:
				eval = self.min_evaluation(
					match.board, piece, pos,
					alpha, beta, 1
				)

				alpha = max(alpha, eval)

			if alpha < beta:
				beta = alpha
				chosen_piece = piece

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(chosen_piece)

		return chosen_piece

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()
		fallback_i = random.randint(0, len(available_pos) - 1)
		better_pos = available_pos[fallback_i]
		alpha, beta = 0, Minimax.EVAL_WIN

		if len(available_pos) >= Minimax.MINIMAX_1_UNTIL and \
				self.max_depth > 1:
			return Minimax(1).putOnBoard(match, piece)
		if len(available_pos) >= Minimax.MINIMAX_2_UNTIL and \
				self.max_depth > 2:
			return Minimax(2).putOnBoard(match, piece)
		if len(available_pos) >= Minimax.MINIMAX_3_UNTIL and \
				self.max_depth > 3:
			return Minimax(3).putOnBoard(match, piece)

		for pos in available_pos:
			eval = self.min_evaluation(
				match.board, piece, pos,
				alpha, beta, 1
			)

			if eval > alpha:
				alpha = eval
				better_pos = pos

		ui.showPlayer(match.active_player)
		ui.showSelectedPosition(better_pos)

		return better_pos
