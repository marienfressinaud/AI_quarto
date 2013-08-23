# -*- coding: utf-8 -*-

def getDiagValues(board, direction):
	val_color = 0
	val_height = 0
	val_shape = 0
	val_consistency = 0

	nb_rows = len(board)
	for i in range(nb_rows):
		piece = None

		if direction == "down":
			piece = board[i][i]
		elif direction == "up":
			piece = board[3 - i][i]

		if not(piece is None):
			val_color += piece.color_int()
			val_height += piece.height_int()
			val_shape += piece.shape_int()
			val_consistency += piece.consistency_int()

	return {
		"color": val_color,
		"height": val_height,
		"shape": val_shape,
		"consistency": val_consistency
	}

def getHVValues(board, direction):
	nb_rows = len(board)
	nb_cols = len(board[0])

	for i in range(nb_rows):
		val_color = 0
		val_height = 0
		val_shape = 0
		val_consistency = 0

		for j in range(nb_cols):
			piece = None
			if direction == "vertical":
				piece = board[i][j]
			elif direction == "horizontal":
				piece = board[j][i]

			if not(piece is None):
				val_color += piece.color_int()
				val_height += piece.height_int()
				val_shape += piece.shape_int()
				val_consistency += piece.consistency_int()

		yield {
			"color": val_color,
			"height": val_height,
			"shape": val_shape,
			"consistency": val_consistency
		}

def getBoardValues(board):
	values = []

	for values_tmp in getHVValues(board, "vertical"):
		values.append(values_tmp)
	for values_tmp in getHVValues(board, "horizontal"):
		values.append(values_tmp)

	values.append(getDiagValues(board, "down"))
	values.append(getDiagValues(board, "up"))

	return values