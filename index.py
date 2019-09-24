#! /usr/bin/env python3
# coding: utf-8

# -tc- ajouter une docstring de module
import json

import requests
import mysql.connector
# -tc- éviter les modules avec des majuscules et des _

from classes.database import Database, CategoryManager, FoodManager, HistoryManager

from classes.terminal import Terminal

# -tc- éviter de structurer un projet python sur un seul module. Chaque partie
# -tc- de l'application doit aller dans son propre module.

# -tc- Le projet doit être structuré selon une logique orientée objet

########################

# -tc- REFACTORING n°1: séparer le code client et la création de la base de
# -tc- données


# -tc- dans une classe Database



# -tc- Utiliser une classe CategoryManager


# -tc- Utiliser une classe FoodManager. Différencier les opérations de
# -tc- remplissage et de tri





# -tc- A partir d'ici, on est dans le code client. Créer une classe Client et
# -tc- transformer les fonctions qui suivent en méthodes de cette classe.
# -tc- Les méthodes du client ne doivent pas utiliser de code SQL directement.
# -tc- Créer des classes FoodManager(), CategoryManager(), FavoriteManager()
# -tc- pour cela.





# -tc- Attention aux fonctions longues. On ne devrait pas dépasser 20 lignes




################################################################################

####################################
# Connecting/creating Database
####################################



####################################
# MAIN
####################################

# -tc- Si c'est la partie principale, créer une fonction main()
def main():
    """Point d'entrée principal du programme."""

    # Creation of the database
    database = Database()
    category_manager = CategoryManager(database)
    food_manager = FoodManager(database)
    history_manager = HistoryManager(database)
    terminal = Terminal ()

    #if database.connected:
    category_manager.filling_category()
    food_manager.sorting_and_filling("Yaourts")
    food_manager.sorting_and_filling("Chocolats")
    food_manager.sorting_and_filling("Boissons")
    food_manager.sorting_and_filling("Snacks")
    food_manager.sorting_and_filling("Produits laitiers")


    ####################################
    # TERMINAL INTERFACE
    ####################################

    option_choice = terminal.option_select()


    if option_choice == 1:

        categ_choice = category_manager.categ_select()

    # PRODUCT SELECT OK
        product_return = food_manager.product_select(categ_choice)
    #    print("01",product_return)
        foodname_selected = product_return[0]
    #    print("\n02",foodname_selected)
        name_id_list = product_return[1]
    #    print("\n03",name_id_list)
        selected_food_id = name_id_list[foodname_selected]
    #    print("\n04",selected_food_id,"\n")
    #########################################################


    # ALTERN SELECT
        altern_return = food_manager.altern_select(categ_choice)
    #    print("\n05", altern_return)
        altern_foodname_selected = altern_return[0]
    #    print("\n06",altern_foodname_selected)
        altern_name_id_list = altern_return[1]
    #    print("\n07",altern_name_id_list)
        altern_selected_food_id = altern_name_id_list[altern_foodname_selected]
    #    print("\n08",altern_selected_food_id,"\n")
    #########################################################

    # ALTERN DISPLAY
        savingdb = food_manager.altern_display(altern_selected_food_id)
    #########################################################

    # SAVE HISTORY
        history_manager.save_history(
            savingdb, selected_food_id, altern_selected_food_id
        )


    elif option_choice == 2:

        history_id_tuple = history_manager.history_display()
    #    true_id = history_id_tuple[0]
    #    print("Z", true_id)
        oldnew_id = history_id_tuple[1]
    #    print("A", oldnew_id)
        surr_old_id = oldnew_id[0]
    #    print("B", surr_old_id)
        surr_new_id = oldnew_id[1]
    #    print("C", surr_new_id)
        history_manager.history_details(surr_old_id, surr_new_id)


    elif option_choice == 3:
        print("Au revoir")

if __name__ == "__main__":
    main()