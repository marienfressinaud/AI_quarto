# -*- coding: utf-8 -*-

def showBoard(board):
	print "  ",
	for j in range(len(board[0])):
		print "%3d   " % (j + 1),
	print
	print "-" * 30,
	print

	for i in range(len(board)):
		print str(i + 1) + "|",
		for j in range(len(board[0])):
			piece = board[i][j]
			if piece is None:
				print "%(pad)5s|" \
				    % { "pad": "" },
			else:
				print "%(piece)4s |" \
				    % { "piece": str(piece) },
		print

def choosePiece(pieces):
	msg = "\nChoose a piece: "
	for p in pieces:
		msg += str(p) + " "
	print msg

def choosePosition():
	print "\nChoose a position (line column)"

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

def endGame(winner):
	print

	if winner is None:
		print "No solution, no winner..."
	else:
		print winner.name, "is the winner!"