# -*- coding: utf-8 -*-

def __get_available_place(board, prop, index, direction):
	pos = None
	is_ok = True

	for i in xrange(len(board)):
		piece = None
		x, y = 0, 0
		if direction == "row":
			piece = board[index][i]
			x, y = index, i
		elif direction == "col":
			piece = board[i][index]
			x, y = i, index
		if direction == "diag-down":
			piece = board[i][i]
			x, y = i, i
		elif direction == "diag-up":
			piece = board[3 - i][i]
			x, y = 3 - i, i

		if is_ok and piece is None:
			pos = {
				"x": x,
				"y": y,
			}
		elif piece is not None and \
				piece.getPropriety(prop["propriety"]) != prop["value"]:
			pos = None
			is_ok = False

	return pos

def __get_diag_values(board, direction):
	val_color = 0
	val_height = 0
	val_shape = 0
	val_state = 0

	nb_rows = len(board)
	for i in xrange(nb_rows):
		piece = None
		if direction == "down":
			piece = board[i][i]
		elif direction == "up":
			piece = board[3 - i][i]

		if piece is not None:
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

def __get_RC_values(board, direction):
	nb_rows = len(board)
	nb_cols = len(board[0])

	for i in xrange(nb_rows):
		val_color = 0
		val_height = 0
		val_shape = 0
		val_state = 0

		for j in xrange(nb_cols):
			piece = None
			if direction == "row":
				piece = board[i][j]
			elif direction == "col":
				piece = board[j][i]

			if piece is not None:
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

def get_board_values(board):
	values = []

	values.extend(__get_RC_values(board, "row"))
	values.extend(__get_RC_values(board, "col"))
	values.append(__get_diag_values(board, "down"))
	values.append(__get_diag_values(board, "up"))

	return values


def maximize_property(board, prop):
	board_values = get_board_values(board)

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
			pos = __get_available_place(board, prop, i, "row")
		elif i < 8:
			pos = __get_available_place(board, prop, i - 4, "col")
		elif i < 9:
			pos = __get_available_place(board, prop, None, "diag-down")
		elif i < 10:
			pos = __get_available_place(board, prop, None, "diag-up")

		if pos == None:
			pass
		elif better_v == None \
		or (v[prop_name] ** 2 > better_v[prop_name] ** 2):
			better_index, better_pos = i, pos

	val_prop = board_values[better_index][prop_name]

	return {
		"position": better_pos,
		"value": val_prop
	}

def get_wining_properties(board):
	props = set()

	for board_values in get_board_values(board):
		if board_values["color"] == -3:
			props.add("red")
		elif board_values["color"] == 3:
			props.add("blue")

		if board_values["height"] == -3:
			props.add("short")
		elif board_values["height"] == 3:
			props.add("tall")

		if board_values["shape"] == -3:
			props.add("round")
		elif board_values["shape"] == 3:
			props.add("square")

		if board_values["state"] == -3:
			props.add("solid")
		elif board_values["state"] == 3:
			props.add("hollow")

	return props

def eval_position(direction, board, pos):
	piece = board[pos["x"]][pos["y"]]
	prop = {
		piece.color: 0,
		piece.height: 0,
		piece.shape: 0,
		piece.state: 0
	}
	nb_pieces = 0
	eval_pos = 0

	winning_props = get_wining_properties(board)
	if ("red" in winning_props and "blue" in winning_props) or \
			("short" in winning_props and "tall" in winning_props) or \
			("round" in winning_props and "square" in winning_props) or \
			("solid" in winning_props and "hollow" in winning_props):
		# two different winning values for a same property,
		# it's like this board has been already won, but not sure
		return 0

	for i in xrange(len(board)):
		x, y = 0, 0

		if direction == "row":
			x, y = pos["x"], i
		elif direction == "col":
			x, y = i, pos["y"]
		elif direction == "diag-down":
			x, y = i, i
		elif direction == "diag-up":
			x, y = i, 3 - i

		cur_piece = board[x][y]
		if cur_piece is not None:
				prop[piece.color] += cur_piece.color_int()
				prop[piece.height] += cur_piece.height_int()
				prop[piece.shape] += cur_piece.shape_int()
				prop[piece.state] += cur_piece.state_int()
				nb_pieces += 1

	prop[piece.color] *= prop[piece.color]
	prop[piece.height] *= prop[piece.height]
	prop[piece.shape] *= prop[piece.shape]
	prop[piece.state] *= prop[piece.state]

	nb_pieces *= nb_pieces

	if prop[piece.color] == nb_pieces:
		eval_pos += 1
	if prop[piece.height] == nb_pieces:
		eval_pos += 1
	if prop[piece.shape] == nb_pieces:
		eval_pos += 1
	if prop[piece.state] == nb_pieces:
		eval_pos += 1

	return eval_pos

def str_from_server(str):
    trad = ""

    if str[0] == "B":
        trad = "b"
    else:
        trad = "r"

    if str[1] == "L":
        trad = trad.upper()

    if str[3] == "H":
        trad = trad + "*"

    if str[2] == "C":
        trad = "(" + trad + ")"

    return trad
