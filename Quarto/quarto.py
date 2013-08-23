#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match

def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''
	configuration = {
		'name_player1': 'Patrick',
		'name_player2': 'Robert',
		'intelligence_player1': None,
		'intelligence_player2': 'Random'
	}
	match = Match(configuration)
	match.run()

if __name__ == "__main__":
	main()