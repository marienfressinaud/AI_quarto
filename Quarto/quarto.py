#!/usr/bin/env python
# -*- coding: utf-8 -*-

from match import Match
from intelligence import Human, Random, Novice

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

	return ("p", "c", "q")

def get_choice(possible_choices = None):
	"""
	Permits to get a choice between different choices as input
	"""

	choice = None
	ok = False

	while not ok:
		choice = raw_input("> ")

		if (possible_choices is None) or \
		   (choice.lower() in possible_choices):
			ok = True
		else:
			message = "Invalid choice, choose between "
			for c in possible_choices:
				message += c.upper() + " or "
			print message[:-3]

	return choice

def change_configuration():
	print "We will now change player configuration"

	configuration = {}

	for i in range(2):
		print "[PLAYER " + str(i + 1) + "]"
		print "What is his name?"
		configuration["name_player" + str(i + 1)] = get_choice()

		print "Is he (H)uman, (R)andom or (N)ovice?"
		choice = get_choice(("h", "r", "n")).lower()

		if choice == "h":
			intelligence = Human()
		elif choice == "r":
			intelligence = Random()
		elif choice == "n":
			intelligence = Novice()

		configuration["intelligence_player" + str(i + 1)] = intelligence

		print

	return configuration


def main():
	'''
	Main function permits to launch a match of Quarto
	It permits also to modify game configuration (mainly players attributes)
	'''

	configuration = {
		'name_player1': 'Qua',
		'name_player2': 'Rto',
		'intelligence_player1': Human(),
		'intelligence_player2': Novice()
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