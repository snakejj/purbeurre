#! /usr/bin/env python3
# coding: utf-8

"""Module which defines all classes and functions related to the terminal
display."""


class Terminal:
    """Class which defines all functions related to the terminal display"""

    def __init__(self):
        """Méthode d'initialisation de la classe"""
        self.integ = False

    def option_select(self):
        """Funtion which displays main options"""

        print("##############################################################")

        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        print("3 - Quitter !")

        while not self.integ:
            try:
                option_choice = input("Enter le n° de l'option souhaité : ")
                option_choice = int(option_choice)
                self.integ = True
                if 0 < option_choice < 4:

                    return option_choice

                else:

                    print("Cette option n'existe pas !")
                    self.integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                self.integ = False
