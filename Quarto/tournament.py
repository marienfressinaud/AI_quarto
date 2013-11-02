# -*- coding: utf-8 -*-

import random
import socket

from match import Match
from message import Message
from models import Board
from util import str_from_server
import ui


class Tournament(Match):

    def __init__(self, configuration):
        super(Tournament, self).__init__(configuration)
        s = None

        hostname = configuration["hostname"]
        if hostname is None:
            hostname = socket.gethostname()

        try:
            s = socket.socket()
            s.connect((hostname, 4455))
        except socket.error, err:
            raise Exception("%s" % err)

        Message._file = s.makefile("r+")

        Message.read_msg()  # skip "Do you want to play a game?"

        message = Message.read_msg()
        self.player_num = message.argv[0]

        if self.player_num == "one":
            self.intelligence = configuration["intelligence_player1"]
        else:
            self.intelligence = configuration["intelligence_player2"]
            self.nextPlayer()

    def run(self):
        message = Message.read_msg()

        while message.type != "GameOver":
            if message.type == "Round":
                self.__new_round(message.argv[1])

            message = Message.read_msg()

    def __new_round(self, first_player):
        self.board = Board()
        turn = 0

        message = Message.read_msg()
        while message.type != "Winner" and message.type != "Invalid":
            if message.type == "Turn":
                pos = None
                selected_piece = None

                if turn == 0 and first_player == self.player_num:
                    pos = {
                        'x': random.randint(0, 4),
                        'y': random.randint(0, 4)
                    }
                    selected_piece = self.intelligence.selectPiece(self)
                else:
                    piece = self.board.getPiece(
                        str_from_server(message.argv[0])
                    )
                    pos = self.intelligence.putOnBoard(self, piece)
                    self.board.putPiece(piece, pos)

                    selected_piece = self.intelligence.selectPiece(self)

                if selected_piece is not None and pos is not None:
                    piece_str = selected_piece.str_server_style()
                    Message.send_move(pos, piece_str)
            elif message.type == "BoardUpdate":
                piece = self.board.getPiece(
                    str_from_server(message.argv[0])
                )
                pos = {
                    'x': int(message.argv[1]),
                    'y': int(message.argv[2])
                }
                self.board.putPiece(piece, pos)
                ui.showBoard(self.board)
            elif message.type == "Invalid":
                print "Oups, an error occured!"
                # TODO exception

            turn += 1
            message = Message.read_msg()
