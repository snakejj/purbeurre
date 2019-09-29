#! /usr/bin/env python3
# coding: utf-8

"""This Module is the main one of the program, which contain the main function
which calls them all"""

from purbeurre.database import Database, CategoryManager
from purbeurre.database import FoodManager, HistoryManager
from purbeurre.terminal import Terminal

###############################################################################

####################################
# MAIN
####################################


def main():

    """Program's main entry point"""

    # Creation of the database
    database = Database()
    category_manager = CategoryManager(database)
    food_manager = FoodManager(database)
    history_manager = HistoryManager(database)
    terminal = Terminal()

    category_manager.filling_category()
    food_manager.isdbempty()
    if food_manager.dbempty:
        print(
            "\nLa base de données est vide, remplissage en cours.\n"
            "L'operation peut prendre quelques minutes, merci de"
            " patienter."
                )
        food_manager.sorting_and_filling("Yaourts")
        food_manager.sorting_and_filling("Chocolats")
        food_manager.sorting_and_filling("Boissons")
        food_manager.sorting_and_filling("Snacks")
        food_manager.sorting_and_filling("Produits laitiers")
    else:
        pass

    ####################################
    # TERMINAL INTERFACE
    ####################################

    option_choice = terminal.option_select()

    if option_choice == 1:

        categ_choice = category_manager.categ_select()

    # PRODUCT SELECT
        product_return = food_manager.product_select(categ_choice)
        foodname_selected = product_return[0]
        name_id_list = product_return[1]
        selected_food_id = name_id_list[foodname_selected]
    #########################################################

    # ALTERN SELECT
        altern_return = food_manager.altern_select(categ_choice)
        altern_foodname_selected = altern_return[0]
        altern_name_id_list = altern_return[1]
        altern_selected_food_id = altern_name_id_list[altern_foodname_selected]
    #########################################################

    # ALTERN DISPLAY
        savingdb = food_manager.altern_display(altern_selected_food_id)
    #########################################################

    # SAVE HISTORY
        history_manager.save_history(
            savingdb, selected_food_id, altern_selected_food_id
        )
    #########################################################

    elif option_choice == 2:
        history_id_tuple = history_manager.history_display()
        oldnew_id = history_id_tuple[1]
        surr_old_id = oldnew_id[0]
        surr_new_id = oldnew_id[1]
        history_manager.history_details(surr_old_id, surr_new_id)

    elif option_choice == 3:
        print("Au revoir")


if __name__ == "__main__":
    main()
