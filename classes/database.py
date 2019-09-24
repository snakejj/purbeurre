#! /usr/bin/env python3
# coding: utf-8

# -tc- ajouter une docstring de module
"""Module which defines all classes and functions related to the database."""



import requests
import json
import mysql.connector
import config

# -tc- éviter les modules avec des majuscules et des _



class Database:
    """Ajouter une docstring."""

    def __init__(self):
        """Méthode d'initialisation de la classe.

        Arguments:
        ==========
        param_a (str): decrire le param_a  
        param_b (int): decrire le param_b      
        """
        self.connected = False
        self.cnx = None

    def get_cursor(self):
        if not self.connected:
            self.connect()
            self.execute_sql_from_file("sql_script_purbeurre.sql")
        return self.cnx.cursor()

    def connect(self):
        """Ajouter une docstring."""

        self.connected = True

        try:
            print("\nConnecting to the database ... \n")

            self.cnx = mysql.connector.connect(
                user=config.USER,
                password=config.PASSWORD,
                host=config.HOST,
                db=config.DB_NAME,
                auth_plugin=config.AUTH_PLUGIN
            )

            print("Connected successfully !\n")

            
        #    print("Cursor opening !\n")

        except mysql.connector.Error:

            print(
                "Failed to connect to the database :" 
                "Database does not exist.\n"
                "Please create a database "
                "and configure its name in config.py !\n"
            )
            print()

            self.cnx = mysql.connector.connect(
                user=config.USER,
                password=config.PASSWORD,
                host=config.HOST,
                auth_plugin=config.AUTH_PLUGIN
            )

        #    print("Cursor opening in else !\n")

        try:
            execute_sql_from_file(cursor, "sql_script_purbeurre.sql")
            print("Database created with success !\n")

        except:
            pass
        
    def execute_sql_from_file(self, filename):
        """Ajouter une doctring"""
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
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            cursor.execute(command) 

class CategoryManager:
    """Ajouter une docstring."""

    def __init__(self, database):
        self.database = database
        
    def filling_category(self):
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()
        
        cursor.execute("""SELECT * FROM Category""")

        rows_count = cursor.fetchall()
        #    print(rows_count)

        if not rows_count:
            try:

                cursor.execute("""INSERT INTO Category (category_name)
                                VALUES
                                ('Yaourts'),
                                ('Chocolats'),
                                ('Boissons'),
                                ('Snacks'),
                                ('Produits laitiers');""")

                print("Categories successfully inserted !")
                print("Chargement en cours, veuillez patienter ...")
                cnx.commit()

            except:

                print("Error while inserting categories in DB")
        else:
            print("Categories already in the DB !")
            print("Chargement en cours, veuillez patienter ...")
    
    def filling_category_db(self,database):
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()

        cursor.execute("""SELECT * FROM Category""")

        rows_count = cursor.fetchall()
        #    print(rows_count)

        if not rows_count:
            try:

                cursor.execute("""INSERT INTO Category (category_name)
                                VALUES
                                ('Yaourts'),
                                ('Chocolats'),
                                ('Boissons'),
                                ('Snacks'),
                                ('Produits laitiers');""")

                print("Categories successfully inserted !")
                print("Chargement en cours, veuillez patienter ...")
                cnx.commit()

            except:

                print("Error while inserting categories in DB")
        else:
            print("Categories already in the DB !")
            print("Chargement en cours, veuillez patienter ...")

    def categ_select(self):
        """Ajouter une doctring"""
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
    """Ajouter une docstring."""

    def __init__(self, database):
        self.database = database

    def sorting_and_filling(self,category):
        """Ajouter une doctring"""
        
        cursor = self.database.get_cursor()
        response = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?search_terms2={}&action=process&json=1&page_size=100".format(category))
        result = json.loads(response.text)
        cursor.execute(
            'SELECT category_id FROM Category WHERE category_name = (%s)', (category,))
        numid = cursor.fetchone()
        #print(numid)

        cursor.execute(
            'SELECT food_id FROM Food WHERE category_id = (%s)', (numid[0],))
        rows_count = cursor.fetchall()
        #print(rows_count)

        if not rows_count:
            try:
                #            print("Row count est vide")

                #    print(numid[0])
                for p in result['products']:
                    if p['code'] and 4 < len(p['product_name_fr']) < 80 and len(p['url']) < 255 and 1 < len(p['stores']) < 150 and p['ingredients_text_fr'] and len(p['nutrition_grades_tags'][0]) == 1:

                        #print(p['nutrition_grades_tags'][0])
                        #print(p['stores'])
                        cursor.execute("INSERT INTO Food (category_id, food_name, ingredients_text, store, off_link, nutriscore) VALUES (%s, %s, %s, %s, %s, %s)", (
                            numid[0], p['product_name_fr'], p['ingredients_text_fr'], p['stores'], p['url'], p['nutrition_grades_tags'][0], ))

                        cnx.commit()
            except:

                print("ERREUR")

        else:
            # -tc- à quoi servent ces print()? Ce n'est pas une bonne idée
            # -tc- d'utiliser des print() pour débugger.
            #            print("else")
            pass

        #        else:
        #            print("Incomplet !")

    def altern_display(self,selected_food_id):
        """Ajouter une doctring"""

        #    altern_choice_str = ''.join(altern_choice)

        #    clean = ["('", "',)"]
        #    for i in clean:
        #        altern_choice_str=altern_choice_str.replace(i, "")
        cursor = self.database.get_cursor()
        cursor.execute('SELECT * FROM Food WHERE food_id = (%s)',
                    (selected_food_id,))
        result = cursor.fetchall()

        #    print("\n\n ###################")
        #    print(result)
        #    print(" ###################\n\n ")

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

    def altern_select(self,numcateg):
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()

        cursor.execute("""
            SELECT food_name, food_id FROM Food WHERE category_id = (%s) 
            AND nutriscore IN(
                SELECT nutriscore FROM Food WHERE nutriscore <= "b"
            )
            ORDER BY RAND() 
            LIMIT 3""", 
            (numcateg,)
        )
        result = cursor.fetchall()

        #    print("Test 1:",result)
        #    print("Test 2:",result[0])
        #    print("Test 3:",result[0][0])
        #    print("Test 4:",result[0][1])
        integ = False
        i = 1
        j = 1
        #    clean = ["(", ",)"]
        list_product = []
        id_list = {}

        for a, b in result:
            id_list.update({a: b})

        #    print(id_list)
        #    print("")
        #    print(list_product)
        #    for a in result:
        #        a = str(a)
        #        for i in clean:
        #            a=a.replace(i, "")

        #        list_product.append(a)

        #    print("GOGOGO :", result)
        #    print(id_list)
        for element in result:

            #        print(i, ":", element[0])
            list_product.append(element[0])
            i += 1

        list_product.sort(key=str.lower)
        for element in list_product:
            print(j, ":", element)
            j += 1
        #    print("COMPLETE PRINT TEST :",list_product)

        #    print(list_product)

        #    print(display,":",a)

        while not integ:
            try:
                altern_choice = input(
                    "Enter le n° du produit alternatif souhaité pour plus d'informations : ")
                altern_choice = int(altern_choice)
                integ = True
                if 0 < altern_choice < 4:
                    #                print("")
                    #                return list_altern[altern_choice-1]
                    product_name = list_product[altern_choice-1]
                    return [product_name, id_list]
                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

    def product_select(self,numcateg):
        """Ajouter une doctring"""

        cursor = self.database.get_cursor()
        cursor.execute(
            'SELECT food_name, food_id FROM Food WHERE category_id = (%s) AND nutriscore >= "c" ORDER BY RAND() LIMIT 10 ', (numcateg,))
        result = cursor.fetchall()

        #    print("Test 1:",result)
        #    print("Test 2:",result[0])
        #    print("Test 3:",result[0][0])
        #    print("Test 4:",result[0][1])
        integ = False
        i = 1
        j = 1
        #    clean = ["(", ",)"]
        list_product = []
        id_list = {}

        for a, b in result:
            id_list.update({a: b})

        #    print(id_list)
        #    print("")
        #    print(list_product)
        #    for a in result:
        #        a = str(a)
        #        for i in clean:
        #            a=a.replace(i, "")

        #        list_product.append(a)

        #    print("GOGOGO :", result)
        for element in result:

            #        print(i, ":", element[0])
            list_product.append(element[0])
            i += 1

        list_product.sort(key=str.lower)
        for element in list_product:
            print(j, ":", element)
            j += 1
        #    print("COMPLETE PRINT TEST :",list_product)

        #    print(list_product)

        #    print(display,":",a)

        while not integ:
            try:
                product_choice = input("Enter le n° du produit souhaité : ")
                product_choice = int(product_choice)
                integ = True
                if 0 < product_choice < 11:
                    print("Recherche de produits alternatifs en cours...\n")
        #                print("")
                    product_name = list_product[product_choice-1]
                    return [product_name, id_list]

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

class HistoryManager:
    """Ajouter une docstring."""

    def __init__(self, database):
        self.database = database

    def history_details(self, old_id, new_id):
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()

        cursor.execute('SELECT * FROM Food WHERE food_id = (%s)', (old_id,))
        old = cursor.fetchall()

        #    print("\n\n ###################")
        #    print(result)
        #    print(" ###################\n\n ")

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
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()

        cursor.execute('SELECT history_id FROM History LIMIT 10')
        idlen = cursor.fetchall()
        last = len(idlen)
        print(last)

        cursor.execute('SELECT * FROM History ORDER BY history_id DESC LIMIT 10')
        result = cursor.fetchall()

        i = 1
        id_list = {}
        food_id_oldnew = []

        print("\nVoici la liste de(s)", last, "derniere(s) substitution(s)")

        for a, b, c in result:

            cursor.execute('SELECT food_name FROM Food WHERE food_id = (%s)', (b,))
            old = cursor.fetchone()
            cursor.execute('SELECT food_name FROM Food WHERE food_id = (%s)', (c,))
            new = cursor.fetchone()
            id_list.update({i: a})
            food_id_oldnew.append([b, c])
            print(i, ":", old[0], "->", new[0])
            i += 1

        #    print("FOOD_ID_OLD_NEW",food_id_oldnew)
        #    print("ID_LIST", id_list)
        integ = False

        while not integ:
            try:
                categ_choice = input("Enter le n° de la substitution souhaité : ")
                categ_choice = int(categ_choice)
                integ = True
                if 0 < categ_choice <= i:

                    oldnew_id = food_id_oldnew[categ_choice-1]
        #                print(oldnew_id)
                    true_id = id_list[categ_choice]
        #                print(true_id)
                    return true_id, oldnew_id

                else:

                    print("Cette option n'existe pas !")
                    integ = False

            except ValueError:
                print("La saisie est incorrect, vous devez tapez un chiffre.")
                integ = False

    def save_history(self,saving, food_id, surrogate_id):
        """Ajouter une doctring"""
        cursor = self.database.get_cursor()

        if saving:

            cursor.execute(
                'INSERT INTO History (food_id,surrogate_id) VALUES ((%s), (%s))', (food_id, surrogate_id,))

            print("Sauvegarde effectuée avec succès !")
            cnx.commit()