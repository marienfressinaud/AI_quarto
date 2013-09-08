#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match
from intelligence import Human, Random, Novice, Minimax
import ui

def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''

	configuration = {
		'name_player1': 'Player 1',
		'name_player2': 'Player 2',
		'intelligence_player1': Novice(),
		'intelligence_player2': Minimax(2)
	}

	match = Match(configuration)

	pieces = match.board.unusedPieces()
	pos = {"x": 0, "y": 0}
	match.board.putPiece(pieces[6], pos)
	pos = {"x": 0, "y": 1}
	match.board.putPiece(pieces[1], pos)
	pos = {"x": 0, "y": 2}
	match.board.putPiece(pieces[8], pos)
	pos = {"x": 0, "y": 3}
	match.board.putPiece(pieces[10], pos)
	pos = {"x": 1, "y": 0}
	match.board.putPiece(pieces[13], pos)
	pos = {"x": 1, "y": 3}
	match.board.putPiece(pieces[7], pos)
	# pos = {"x": 2, "y": 0}
	# match.board.putPiece(pieces[5], pos)
	pos = {"x": 2, "y": 2}
	match.board.putPiece(pieces[2], pos)
	pos = {"x": 3, "y": 2}
	match.board.putPiece(pieces[0], pos)

	ui.showBoard(match.board)
	ui.showChoosePiece(match.board.unusedPieces())

	# print pieces[15]
	# Minimax(1).putOnBoard(match, pieces[15])

	Minimax(1).selectPiece(match)

	print Minimax(1).evaluation(match.board, pos)

if __name__ == "__main__":
	main()
