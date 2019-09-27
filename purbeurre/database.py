#! /usr/bin/env python3
# coding: utf-8

"""Module which defines all classes and functions related to the database."""

import requests
import json
import mysql.connector
import sys

import config


class Database:
    """Class which defines all functions related to the database"""

    def __init__(self):
        """Initialization's method of the Database's class"""
        self.connected = False
        self.cnx = None

    def get_cursor(self):
        """Method which returns the cursor"""
        if not self.connected:
            self.connect()
            self.execute_sql_from_file("sql_script_purbeurre.sql")
        return self.cnx.cursor()

    def execute_sql_from_file(self, filename):
        """Method which execute SQL requests from a file"""
        # Open and read the file as a single buffer
        cursor = self.cnx.cursor()
        with open(filename, 'r') as fd:
            sql_file = fd.read()

        # Get rid of commentary and ends-lines
        sql_file = "".join(
            line for line in sql_file.split("\n")
            if not line.startswith('--')
        )

        # Get rid of empty lines
        sql_commands = [
            line.strip() for line in sql_file.split(";")
            if line.strip()
        ]

        # Execute every command from the input file
        for command in sql_commands:
            cursor.execute(command)

    def connect(self):
        """Method which try to connect to database, if it can't it will ask
        to create the database and to put the credentials in the file
        config.py."""

        self.connected = True

        try:
            print("\nConnexion à la base de données ... \n")

            self.cnx = mysql.connector.connect(
                user=config.USER,
                password=config.PASSWORD,
                host=config.HOST,
                db=config.DB_NAME,
                auth_plugin=config.AUTH_PLUGIN
            )

            print("Connexion effectué avec succès !\n")

        except mysql.connector.Error:

            print(
                "Impossible de se connecter à la base de données : "
                "La base de données n'existe pas.\n"
                "Merci de créer une base de données et d'editer le fichier "
                "config.py avec les differentes informations de connexion !\n"
            )

            sys.exit()

        try:
            execute_sql_from_file(cursor, "sql_script_purbeurre.sql")
        except NameError:
            pass


class CategoryManager:
    """Class which defines all functions related to the table Category"""

    def __init__(self, database):
        """Initialization's method of the CategoryManager's class"""
        self.database = database

    def filling_category(self):
        """Function which fills the category table"""

        cursor = self.database.get_cursor()
        cursor.execute("""SELECT * FROM Category""")
        rows_count = cursor.fetchall()

        if not rows_count:
            try:

                cursor.execute("""INSERT INTO Category (category_name)
                                VALUES
                                ('Yaourts'),
                                ('Chocolats'),
                                ('Boissons'),
                                ('Snacks'),
                                ('Produits laitiers');""")

                print(
                    "Chargement en cours...\n"
                    "Le chargement peut prendre quelques minutes, merci de"
                    "patienter"
                    )
                self.database.cnx.commit()

            except NameError:

                print(
                    "Erreur lors de l'insertion des catégories dans la"
                    "base de données"
                )
        else:
            print(
                    "Chargement en cours...\n"
                    "Le chargement peut prendre quelques minutes, merci de "
                    "patienter."
                )

    def categ_select(self):
        """Funtion which displays the differents categories and asks to select
        one"""
        cursor = self.database.get_cursor()

        cursor.execute('SELECT * FROM Category')
        result = cursor.fetchall()
        for a, b in result:
            print(a, ":", b)

        integ = False

        while not integ:
            try:
                categ_choice = input("Enter le n° de la categorie souhaité : ")
                categ_choice = int(categ_choice)
                integ = True
                if 0 < categ_choice < 6:

                    return categ_choice

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False


class FoodManager:
    """Class which defines all functions related to the table Food"""

    def __init__(self, database):
        """Initialization's method of the FoodManager's class"""
        self.database = database

    def sorting_and_filling(self, category):
        """Funtion which make the api request, put all the datas in a variable,
        then sort it so that only products with all the fields needed within
        a certain limit of character length will then filled into the
        database"""

        cursor = self.database.get_cursor()

        url = "https://fr.openfoodfacts.org/cgi/search.pl"

        data = {
            "action": "process",
            "json": 1,
            "page_size": 1000,
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans_n",
        }

        response = requests.get(url, params=data)
        result = json.loads(response.text)

        cursor.execute(
            'SELECT category_id FROM Category WHERE category_name = (%s)', (
                category,)
            )
        numid = cursor.fetchone()

        cursor.execute(
            'SELECT food_id FROM Food WHERE category_id = (%s)', (numid[0],)
            )
        rows_count = cursor.fetchall()

        if not rows_count:
            try:
                for p in result['products']:
                    if (p.get('code', "") and
                        4 < len(p.get('product_name_fr', "")) < 80 and
                        len(p.get('url', "")) < 255 and
                        1 < len(p.get('stores', "")) < 150 and
                        p.get('ingredients_text_fr', "") and
                            len(p.get('nutrition_grades_tags', "")[0]) == 1):

                        cursor.execute(
                            """
                            INSERT INTO Food (
                                category_id,
                                food_name,
                                ingredients_text,
                                store,
                                off_link,
                                nutriscore
                                )
                            VALUES (%s, %s, %s, %s, %s, %s)""", (
                                numid[0],
                                p['product_name_fr'],
                                p['ingredients_text_fr'],
                                p['stores'],
                                p['url'],
                                p['nutrition_grades_tags'][0],
                                )
                            )

                        self.database.cnx.commit()
                    else:
                        pass

            except KeyError:

                print(
                    "Erreur lors de l'insertion des produits en base de"
                    "données"
                    )

        else:
            pass

    def product_select(self, numcateg):
        """Function which displays 10 products randomly from the database,
        with a nutriscore of C or worse"""

        cursor = self.database.get_cursor()
        cursor.execute(
            """
            SELECT food_name, food_id
            FROM Food WHERE category_id = (%s) AND nutriscore >= "c"
            ORDER BY RAND() LIMIT 10
            """, (numcateg,)
            )

        result = cursor.fetchall()
        integ = False
        i = 1
        j = 1
        list_product = []
        id_list = {}

        for a, b in result:
            id_list.update({a: b})

        for element in result:
            list_product.append(element[0])
            i += 1

        list_product.sort(key=str.lower)
        for element in list_product:
            print(j, ":", element)
            j += 1

        while not integ:
            try:
                product_choice = input("Enter le n° du produit souhaité : ")
                product_choice = int(product_choice)
                integ = True
                if 0 < product_choice < 11:
                    print("Recherche de produits alternatifs en cours...\n")
                    product_name = list_product[product_choice-1]
                    return [product_name, id_list]

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

    def altern_select(self, numcateg):
        """Functions which displays 3 surrogates for the previously selected
        food, randomly"""
        cursor = self.database.get_cursor()

        cursor.execute(
            """
            SELECT food_name, food_id FROM Food WHERE category_id = (%s)
            AND nutriscore IN(
                SELECT nutriscore FROM Food WHERE nutriscore <= "b"
            )
            ORDER BY RAND()
            LIMIT 3
            """, (numcateg,)
        )
        result = cursor.fetchall()

        integ = False
        i = 1
        j = 1
        list_product = []
        id_list = {}

        for a, b in result:
            id_list.update({a: b})

        for element in result:
            list_product.append(element[0])
            i += 1

        list_product.sort(key=str.lower)
        for element in list_product:
            print(j, ":", element)
            j += 1

        while not integ:
            try:
                altern_choice = input(
                    "Enter le n° du produit alternatif souhaité"
                    "pour plus d'informations : "
                    )

                altern_choice = int(altern_choice)
                integ = True

                if 0 < altern_choice < j:
                    product_name = list_product[altern_choice-1]
                    return [product_name, id_list]

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

    def altern_display(self, selected_food_id):
        """Function which displays the informations of the surrogate and
        letting the user to save the surrogate of the food he previously
        selected"""

        cursor = self.database.get_cursor()
        cursor.execute(
            'SELECT * FROM Food WHERE food_id = (%s)', (selected_food_id,)
            )
        result = cursor.fetchall()

        print("Voici la liste des informations pour ce produit :")
        print("")
        print("Nom du produit :", result[0][2])
        print("Disponible dans ce(s) magasin(s) :", result[0][4])
        print("Lien Open Food Fact :", result[0][5])
        print("Liste des ingredients :", result[0][3])
        print("Nutriscore (a-e) :", result[0][6])

        integ = False

        print("\nSouhaitez vous sauvegarder cette alternative ?")
        print("1 - Oui")
        print("2 - Non")

        while not integ:
            try:
                option_choice = input("Enter le n° de l'option souhaité : ")
                option_choice = int(option_choice)
                integ = True
                if option_choice == 1:
                    saving = True
                    return saving

                elif option_choice == 2:
                    print("Bonne journée, et à bientôt !")
                    saving = False
                    return saving

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False


class HistoryManager:
    """Class which defines all functions related to the table History"""

    def __init__(self, database):
        """Initialization's method of the HistoryManager's class"""
        self.database = database

    def history_details(self, old_id, new_id):
        """Function which displays the food and surrogate associated
        informations, saved with the function "altern_display" in class
        FoodManager"""
        cursor = self.database.get_cursor()

        cursor.execute('SELECT * FROM Food WHERE food_id = (%s)', (old_id,))
        old = cursor.fetchall()

        print("\n\nVoici la liste des informations pour le produit :\n")
        print("Nom du produit :", old[0][2])
        print("Disponible dans ce(s) magasin(s) :", old[0][4])
        print("Lien Open Food Fact :", old[0][5])
        print("Liste des ingredients :", old[0][3])
        print("Nutriscore (a-e) :", old[0][6])

        cursor.execute('SELECT * FROM Food WHERE food_id = (%s)', (new_id,))
        new = cursor.fetchall()

        print("\nVoici la liste des informations pour le substitut :\n")
        print("Nom du produit :", new[0][2])
        print("Disponible dans ce(s) magasin(s) :", new[0][4])
        print("Lien Open Food Fact :", new[0][5])
        print("Liste des ingredients :", new[0][3])
        print("Nutriscore (a-e) :", new[0][6])
        print("")

    def history_display(self):
        """Functions which displays the last subsitutions saved"""
        cursor = self.database.get_cursor()

        cursor.execute('SELECT history_id FROM History LIMIT 10')
        idlen = cursor.fetchall()
        last = len(idlen)
        print(last)

        cursor.execute(
            """
            SELECT * FROM History ORDER BY history_id DESC LIMIT 10
            """
            )
        result = cursor.fetchall()

        i = 1
        id_list = {}
        food_id_oldnew = []

        print("\nVoici la liste de(s)", last, "derniere(s) substitution(s)")

        for a, b, c in result:

            cursor.execute(
                """
                SELECT food_name FROM Food WHERE food_id = (%s)""", (b,)
                )
            old = cursor.fetchone()
            cursor.execute(
                """SELECT food_name FROM Food WHERE food_id = (%s)""", (c,)
                )
            new = cursor.fetchone()
            id_list.update({i: a})
            food_id_oldnew.append([b, c])
            print(i, ":", old[0], "->", new[0])
            i += 1

        integ = False

        while not integ:
            try:
                categ_choice = input(
                    "Enter le n° de la substitution souhaité : "
                    )
                categ_choice = int(categ_choice)
                integ = True
                if 0 < categ_choice <= i:

                    oldnew_id = food_id_oldnew[categ_choice-1]
                    true_id = id_list[categ_choice]
                    return true_id, oldnew_id

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

    def save_history(self, saving, food_id, surrogate_id):
        """Functions which inserts informations about the food and surrogate"""
        cursor = self.database.get_cursor()

        if saving:

            cursor.execute(
                """
                INSERT INTO History (food_id,surrogate_id)
                VALUES ((%s), (%s))""", (food_id, surrogate_id,)
                )

            print("Sauvegarde effectuée avec succès !")
            self.database.cnx.commit()
