# -*- coding: utf-8 -*-


class Message():
    _file = None

    def __init__(self, msg):
        msg = msg[:-1]

        split_msg = msg.split(' ')
        self.type = split_msg[0]
        self.argv = split_msg[1:]

    def __str__(self):
        return ' '.join([self.type] + self.argv)

    def read_msg(cls):
        if Message._file is None:
            return Message("Invalid invalid\n")

        msg = Message._file.readline()
        return Message(msg)

    def send_move(cls, pos, piece):
        if Message._file is None:
            return None

        msg = "Move %d %d %s\n" % (pos['x'], pos['y'], piece)
        Message._file.write(msg)
        Message._file.flush()

    read_msg = classmethod(read_msg)
    send_move = classmethod(send_move)
