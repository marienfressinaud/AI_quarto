#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match
from intelligence import Human, Random, Novice, Minimax

import ui

def change_configuration():
	configuration = {}

	for i in range(2):
		player_conf = ui.askConfPlayer(i + 1)

		intelligence = None
		if player_conf["intelligence"] == "h":
			intelligence = Human()
		elif player_conf["intelligence"] == "r":
			intelligence = Random()
		elif player_conf["intelligence"] == "n":
			intelligence = Novice()
		elif player_conf["intelligence"] == "m":
			intelligence = Minimax(player_conf["depth"])

		configuration["name_player" + str(i + 1)] = player_conf["name"]
		configuration["intelligence_player" + str(i + 1)] = intelligence

	return configuration

def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''

	configuration = {
		'name_player1': 'Player 1',
		'name_player2': 'Player 2',
		'intelligence_player1': Human(),
		'intelligence_player2': Minimax(1)
	}

	choice = None

	while choice != "q":
		ui.showMenu()
		choice = ui.askChoice(("p", "c", "q")).lower()

		if choice == "p":
			match = Match(configuration)
			match.run()
		elif choice == "c":
			configuration = change_configuration()

if __name__ == "__main__":
	main()
