#! /usr/bin/env python3
# coding: utf-8

""" Module which allows to create the database """

import mysql.connector

from config import USER, PASSWORD, HOST, DB_NAME, AUTH_PLUGIN


def execute_sql(cursor):
    """Method which execute SQL requests"""
    # Open and read the requests as a single buffer
    sqlrequests = """
    CREATE SCHEMA IF NOT EXISTS `PurBeurre` ;
    USE `PurBeurre` ;
        """

    # Get rid of commentary and ends-lines
    sqlrequests = "".join(
        line for line in sqlrequests.split("\n") if not line.startswith('--')
        )

    # Get rid of empty lines
    sqlCommands = [
        line.strip() for line in sqlrequests.split(";") if line.strip()
        ]

    # Execute every command from the input file
    for command in sqlCommands:
        cursor.execute(command)

###############################################################################

####################################
# Connecting/creating Database
####################################


try:

    print("\nVerification de l'existance de la base de données ...\n")

    cnx = mysql.connector.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  db=DB_NAME,
                                  auth_plugin=AUTH_PLUGIN)

    print("La base de données existe déja !\n")
    cursor = cnx.cursor()

except mysql.connector.Error as error:

    print(
        "La base de données n'existe pas\n"
        "Creation de la base de données ...\n"
        )
    cnx = mysql.connector.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  auth_plugin=AUTH_PLUGIN)

    cursor = cnx.cursor()

    try:
        execute_sql(cursor)
        print("Base de données crées avec succès !\n")

    except NameError:

        print(
            "Erreur lors de la création de la base de données,"
            " merci de contacter un administrateur."
        )
