# -*- coding: utf-8 -*-

def getAvailablePlaceHV(board, prop, index, direction):
	pos = None
	is_ok = True

	for i in range(len(board)):
		piece = None
		x, y = 0, 0
		if direction == "horizontal":
			piece = board[index][i]
			x, y = index, i
		elif direction == "vertical":
			piece = board[i][index]
			x, y = i, index

		if is_ok and piece is None:
			pos = {
				"x": x,
				"y": y,
			}
		elif not (piece is None) \
		and piece.getPropriety(prop["propriety"]) != prop["value"]:
			pos = None
			is_ok = False

	return pos

def getAvailablePlaceDiag(board, prop, direction):
	pos = None
	is_ok = True

	for i in range(len(board)):
		piece = None
		x, y = 0, 0
		if direction == "down":
			piece = board[i][i]
			x, y = i, i
		elif direction == "up":
			piece = board[3 - i][i]
			x, y = 3 - i, i

		if is_ok and piece is None:
			pos = {
				"x": x,
				"y": y,
			}
		elif not (piece is None) \
		and piece.getPropriety(prop["propriety"]) != prop["value"]:
			pos = None
			is_ok = False
	return pos

def getDiagValues(board, direction):
	val_color = 0
	val_height = 0
	val_shape = 0
	val_state = 0

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
			val_state += piece.state_int()

	return {
		"color": val_color,
		"height": val_height,
		"shape": val_shape,
		"state": val_state
	}

def getHVValues(board, direction):
	nb_rows = len(board)
	nb_cols = len(board[0])

	for i in range(nb_rows):
		val_color = 0
		val_height = 0
		val_shape = 0
		val_state = 0

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
				val_state += piece.state_int()

		yield {
			"color": val_color,
			"height": val_height,
			"shape": val_shape,
			"state": val_state
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

	prop_name = prop["propriety"]
	prop_val = prop["value"]

	better_index = -1
	better_pos = None

	for i in xrange(len(board_values)):
		better_v = None
		if better_index > -1:
			better_v = board_values[better_index]
		v = board_values[i]

		pos = None
		if i < 4:
			pos = getAvailablePlaceHV(board, prop, i, "horizontal")
		elif i < 8:
			pos = getAvailablePlaceHV(board, prop, i - 4, "vertical")
		elif i < 9:
			pos = getAvailablePlaceDiag(board, prop, "down")
		elif i < 10:
			pos = getAvailablePlaceDiag(board, prop, "up")

		if pos == None:
			pass
		elif better_v == None \
		or (v[prop_name] > better_v[prop_name] \
			and (prop_val == "blue" or prop_val == "tall" \
			or prop_val == "square" or prop_val == "hollow") \
		) or (v[prop_name] < better_v[prop_name] \
			and (prop_val == "red" or prop_val == "short" \
			or prop_val == "round" or prop_val == "solid") \
		):
			better_index, better_pos = i, pos

	val_prop = board_values[better_index][prop_name]

	return {
		"position": better_pos,
		"value": val_prop
	}