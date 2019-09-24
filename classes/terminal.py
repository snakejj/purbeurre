#! /usr/bin/env python3
# coding: utf-8

# -tc- ajouter une docstring de module
"""Module which defines all classes and functions related to the terminal
display."""



import requests
import json
import mysql.connector
import config

class Terminal:
    """Ajouter une docstring."""

    def __init__(self):
        """Méthode d'initialisation de la classe.

        Arguments:
        ==========
        param_a (str): decrire le param_a  
        param_b (int): decrire le param_b      
        """
        pass

    def option_select(self):
        """Ajouter une doctring"""

        print("##############################################################")

        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        print("3 - Quitter !")

        integ = False

        while not integ:
            try:
                option_choice = input("Enter le n° de l'option souhaité : ")
                option_choice = int(option_choice)
                integ = True
                if 0 < option_choice < 4:

                    return option_choice

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False
