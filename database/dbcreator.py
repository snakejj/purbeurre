#! /usr/bin/env python3
# coding: utf-8

""" Module which allows to create the database """

import mysql.connector

from configdb import USER, PASSWORD, HOST, DB_NAME, AUTH_PLUGIN, PORT


def execute_sql(cursor, name_of_database):
    """Method which execute SQL requests"""
    # Open and read the requests as a single buffer
    sqlrequest1 = "CREATE SCHEMA IF NOT EXISTS %s" % name_of_database
    sqlrequest2 = "USE %s" % name_of_database

    sqlcommands = [sqlrequest1, sqlrequest2]

    # Execute every command from the input file
    for request in sqlcommands:
        cursor.execute(request)

###############################################################################

####################################
# Connecting/creating Database
####################################


def main():

    try:

        print("\nVerification de l'existance de la base de données ...\n")

        cnx = mysql.connector.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            db=DB_NAME,
            auth_plugin=AUTH_PLUGIN,
            port=PORT
            )

        print("La base de données", DB_NAME, "existe déja !\n")
        cursor = cnx.cursor()

    except mysql.connector.Error:

        print(
            "La base de données n'existe pas\n"
            "Creation de la base de données ...\n"
            )
        cnx = mysql.connector.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            auth_plugin=AUTH_PLUGIN,
            port=PORT
            )

        cursor = cnx.cursor()

        try:
            execute_sql(cursor, DB_NAME)
            print("La base de données", DB_NAME, "à été crée avec succès !\n")

        except NameError:

            print(
                "Erreur lors de la création de la base de données,"
                " merci de contacter un administrateur."
            )


if __name__ == "__main__":
    main()
