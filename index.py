#! /usr/bin/env python3
# coding: utf-8

import requests
import json
import mysql.connector
from config import M_user,M_password

########################

def execute_scripts_from_file(cursor,filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

   

    # Get rid of commentary and ends-lines
    sqlFile = "".join(line for line in sqlFile.split("\n")\
    if not line.startswith('--'))

    # Get rid of empty lines
    sqlCommands = [line.strip() for line in sqlFile.split(";") if line.strip()]

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        
        print(command)
        cursor.execute(command)
        print("Command executed")

########################




cnx = mysql.connector.connect\
(user=M_user, password=M_password, host='localhost',\
auth_plugin='mysql_native_password')
cursor = cnx.cursor()

execute_scripts_from_file(cursor, "sql_script_purbeurre.sql")

#Sorting data

response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms2=Yaourts&action=process&json=1&page_size=20")

result = json.loads(response.text)

for p in result['products'] :
    if p['product_name_fr'] and p['url'] and p['stores'] and p['ingredients_text_fr'] :
        print("Le produit a tout les criteres, merci de remplacer ce print par un INSERT")
        #Launch a function which would INSERT INTO Food ...
    else:
        print("non dispo") 


#############




cursor.close()
cnx.close()


