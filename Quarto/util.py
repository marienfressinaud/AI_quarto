# -*- coding: utf-8 -*-

def getAvailablePlaceHV(board, index, direction):
	for i in range(len(board[0])):
		piece = None
		x, y = 0, 0
		if direction == "horizontal":
			piece = board[index][i]
			x, y = index, i
		elif direction == "vertical":
			piece = board[i][index]
			x, y = i, index

		if piece is None:
			return {
				"x": x,
				"y": y,
			}
	return None

def getAvailablePlaceDiag(board, direction):
	for i in range(len(board)):
		piece = None
		x, y = 0, 0
		if direction == "down":
			piece = board[i][i]
			x, y = i, i
		elif direction == "up":
			piece = board[3 - i][i]
			x, y = 3 - i, i

		if piece is None:
			return {
				"x": x,
				"y": y,
			}
	return None

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

def maximizeProperty(board, prop):
	board_values = getBoardValues(board)

	better_index = -1
	better_pos = None

	for i in xrange(len(board_values)):
		better_v = None
		if better_index > -1:
			better_v = board_values[better_index]
		v = board_values[i]

		pos = None
		if i < 4:
			pos = getAvailablePlaceHV(board, i, "vertical")
		elif i < 8:
			pos = getAvailablePlaceHV(board, i - 4, "horizontal")
		elif i < 9:
			pos = getAvailablePlaceDiag(board, "down")
		elif i < 10:
			pos = getAvailablePlaceDiag(board, "up")

		if pos == None:
			pass
		elif better_v == None \
		or (prop == "blue" and v["color"] > better_v["color"]) \
		or (prop == "red" and v["color"] < better_v["color"]) \
		or (prop == "tall" and v["height"] > better_v["height"]) \
		or (prop == "short" and v["height"] < better_v["height"]) \
		or (prop == "square" and v["shape"] > better_v["shape"]) \
		or (prop == "round" and v["shape"] < better_v["shape"]) \
		or (prop == "hollow" and v["consistency"] > better_v["consistency"]) \
		or (prop == "solid" and v["consistency"] < better_v["consistency"]):
			better_index, better_pos = i, pos

	val_prop = None
	if prop == "blue" or prop == "red":
		val_prop = board_values[better_index]["color"]
	elif prop == "tall" or prop == "short":
		val_prop = board_values[better_index]["height"]
	elif prop == "round" or prop == "square":
		val_prop = board_values[better_index]["shape"]
	elif prop == "hollow" or prop == "solid":
		val_prop = board_values[better_index]["consistency"]

	return {
		"position": better_pos,
		"value": val_prop
	}