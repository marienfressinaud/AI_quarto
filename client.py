# -*- coding: utf-8 -*-

import socket
from sys import exit

from Quarto.match import Match
from Quarto.intelligence import Novice
from Quarto.socket.message import Message
import Quarto.ui as ui

sock = None
my_player_num = None
my_intelligence = Novice()

def translate_piece(str):
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

def new_round(first_player):
    conf_jam = {
        'name_player1': 'Player 1',
        'name_player2': 'Player 2',
        'intelligence_player1': None,
        'intelligence_player2': None
    }

    match = Match(conf_jam)
    turn = 0
    
    message = Message.read_msg(sock)
    while message.type != "Winner":
        if message.type == "Turn":
            pos = None
            selected_piece = None

            if turn == 0 and first_player == my_player_num:
                pos = {
                    'x': 0,
                    'y': 0
                }
                selected_piece = my_intelligence.selectPiece(match)
            else:
                piece = match.board.getPiece(translate_piece(message.argv[0]))
                pos = my_intelligence.putOnBoard(match, piece)
                match.board.putPiece(piece, pos)

                selected_piece = my_intelligence.selectPiece(match)

            piece_str = selected_piece.str_server_style()
            Message.send_move(sock, pos, piece_str)
        elif message.type == "BoardUpdate":
            piece = match.board.getPiece(translate_piece(message.argv[0]))
            pos = {
                'x': int(message.argv[1]),
                'y': int(message.argv[2])
            }
            match.board.putPiece(piece, pos)
        elif message.type == "Invalid":
            print "Oups, an error occured!"
            # TODO exception

        turn += 1
        message = Message.read_msg(sock)

def start_tournament():
    message = Message.read_msg(sock)

    while message.type != "GameOver":
        if message.type == "Round":
            print message.type, message.argv[0]
            new_round(message.argv[1])

        message = Message.read_msg(sock)

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print "Failed to create socket."
        exit(-1)

    print "Socket created"

    sock.connect((socket.gethostname(), 4455))

    print "Socket connected to", socket.gethostname()

    Message.read_msg(sock) # skip "Do you want to play a game?"

    message = Message.read_msg(sock)
    my_player_num = message.argv[0]

    start_tournament()

    sock.close()

if __name__ == "__main__":
    main()