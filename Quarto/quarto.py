#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match
from intelligence import Random

def print_menu():
	"""
	Print game menu and return valid arguments we should take in account
	"""

	print """
	======= MENU =======
	= (P)lay           =
	= (C)onfiguration  =
	= (Q)uit           =
	"""

	return ["p", "c", "q"]

def get_choice(possible_choices):
	"""
	Permits to get a choice between different choices as input
	"""

	choice = None
	ok = False

	while not ok:
		choice = raw_input("> ").lower()

		if choice in possible_choices:
			ok = True
		else:
			message = "Invalid choice, choose between "
			for c in possible_choices:
				message += c.upper() + " or "
			print message[:-3]

	return choice

def change_configuration():
	print "Not implemented"

def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''

	configuration = {
		'name_player1': 'Qua',
		'name_player2': 'Rto',
		'intelligence_player1': None,
		'intelligence_player2': Random()
	}

	choice = None

	while choice != "q":
		possible_choices = print_menu()
		choice = get_choice(possible_choices).lower()

		if choice == "p":
			match = Match(configuration)
			match.run()
		elif choice == "c":
			configuration = change_configuration()

	print "Bye bye!"

if __name__ == "__main__":
	main()