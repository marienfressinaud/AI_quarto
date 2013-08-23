#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match

configuration = {
	'name_player1': 'Qua',
	'name_player2': 'Rto',
	'intelligence_player1': None,
	'intelligence_player2': None
}

def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''

	match = Match(configuration)
	match.run()

if __name__ == "__main__":
	main()