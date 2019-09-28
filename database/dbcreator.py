#! /usr/bin/env python3
# coding: utf-8

""" Module which allows to create the database """

import mysql.connector

from config import USER, PASSWORD, HOST, DB_NAME, AUTH_PLUGIN


def execute_sql_from_file(cursor, filename):
    """Ajouter une doctring"""
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # Get rid of commentary and ends-lines
    sqlFile = "".join(line for line in sqlFile.split("\n")
                      if not line.startswith('--'))

    # Get rid of empty lines
    sqlCommands = [line.strip() for line in sqlFile.split(";") if line.strip()]

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
        execute_sql_from_file(cursor, "createdb.sql")
        print("Base de données crées avec succès !\n")

    except NameError:

        print(
            "Erreur lors de la création de la base de données,"
            " merci de contacter un administrateur."
        )
