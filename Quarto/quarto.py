#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

from match import Match
from tournament import Tournament
from intelligence import Human, Random, Novice, Minimax
import ui


def change_configuration():
    configuration = {}

    for i in xrange(2):
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

    configuration["hostname"] = None
    if len(argv) == 2:
        configuration["hostname"] = argv[1]

    return configuration


def main():
    '''
    Main function permits to launch a match of Quarto
    It permits also to modify game configuration (mainly players attributes)
    '''

    hostname = None
    if len(argv) == 2:
        hostname = argv[1]

    configuration = {
        'name_player1': 'Mr. R',
        'name_player2': 'Mr. N',
        'intelligence_player1': Minimax(3),
        'intelligence_player2': Minimax(4),
        'hostname': hostname
    }

    choice = None

    while choice != "q":
        ui.showMenu()
        try:
            choice = ui.askChoice(("p", "t", "c", "q")).lower()
        except EOFError:
            choice = "q"

        if choice == "p":
            match = Match(configuration)
            match.run()
        elif choice == "t":
            try:
                tournament = Tournament(configuration)
                tournament.run()
            except Exception, e:
                print e
        elif choice == "c":
            configuration = change_configuration()


if __name__ == "__main__":
    main()
