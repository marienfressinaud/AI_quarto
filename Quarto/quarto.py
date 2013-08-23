#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Piece
from models import Player

def main():
	properties = {
		'color': 'blue',
		'size': 'small',
		'shape': 'round',
		'consistency': 'hole'
	}
	piece = Piece(properties)
	print piece.color

	player = Player("Patrick", None)
	print player.name
	if player.isAI:
		print "Player has an artificial intelligence"
	else:
		print "Player is a human"

	print "Not implemented"

if __name__ == "__main__":
	main()