#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from config import M_user,M_password

########################

def execute_scripts_from_file(cursor,filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()


    # Eliminer les commantaires et les fin de ligne
    sqlFile = "".join(line for line in sqlFile.split("\n") if not line.startswith('--'))

    # Eliminer les lignes vides
    sqlCommands = [line.strip() for line in sqlFile.split(";") if line.strip()]

    # Execute every command from the input file
    for command in sqlCommands:

        print(command)
        cursor.execute(command)
        print("Command executed")

########################




cnx = mysql.connector.connect\
(user=M_user, password=M_password, host='localhost')
cursor = cnx.cursor()


execute_scripts_from_file(cursor, "sql_script_purbeurre.sql")

cursor.close()
cnx.close()


