# -*- coding: utf-8 -*-

import socket

class Message():

    def __init__(self, msg):
        split_msg = msg.split(' ')
        self.type = split_msg[0]
        self.argv = split_msg[1:]

        # skip the last \n
        if len(self.argv) > 0:
            self.argv[-1] = self.argv[-1][:-1]
        else:
            self.type = self.type[:-1]

    def __str__(self):
        return ' '.join([self.type] + self.argv)

    def read_msg(cls, sock):
        if sock is None:
            return Message("Invalid\n")

        msg = sock.recv(1024)
        return Message(msg)

    def send_move(cls, sock, pos, piece):
        msg = "Move %d %d %s" % (pos['x'], pos['y'], piece)
        sock.sendall(msg)

    read_msg = classmethod(read_msg)
    send_move = classmethod(send_move)