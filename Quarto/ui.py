# -*- coding: utf-8 -*-

def selectPiece(match):
	pieces = match.getUnusedPieces()
	available_pieces = [str(p) for p in pieces]

	choice = None
	ok = False

	while not ok:
		choice = raw_input("> ")

		if choice in available_pieces:
			ok = True
		else:
			message = "Invalid choice, choose between "
			for c in available_pieces:
				message += c + " or "
			print message[:-3]

	for piece in pieces:
		if str(piece) == choice:
			return piece
	return None

def putOnBoard(match):
	positions = match.getUnusedPositions()

	position = None
	ok = False

	while not ok:
		choice = raw_input("> ").split(" ")
		if len(choice) == 2:
			try:
				pos_tmp = [int(x) for x in choice]
				position = {
					"x": pos_tmp[0] - 1,
					"y": pos_tmp[1] - 1,
				}

				if position in positions:
					ok = True
				else:
					print "Invalid position"
			except:
				print "Invalid position"
		else:
			print "Invalid position"

	return position