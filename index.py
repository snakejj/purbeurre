#! /usr/bin/env python3
# coding: utf-8

import requests
import json
import mysql.connector
from config import M_user,M_password

########################


def execute_sql_from_file(cursor,filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

   

    # Get rid of commentary and ends-lines
    sqlFile = "".join(line for line in sqlFile.split("\n")\
    if not line.startswith('--'))

    # Get rid of empty lines
    sqlCommands = [line.strip() for line in sqlFile.split(";") if line.strip()]
    command_number = 1
    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        
        try:
            cursor.execute(command)
        except OperationalError as error:
            print("Command skipped:",command_number,"{}".format(error))



def sorting_product(category):

    response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms2={}&action=process&json=1&page_size=20".format(category))

    result = json.loads(response.text)

    for p in result['products'] :
        if p['product_name_fr'] and p['url'] and p['stores'] and p['ingredients_text_fr'] and p['nutrition_grades_tags'] :
            print("Disponible.")
            #Launch a function which would INSERT INTO Food ...
        else:
            print("Incomplet !") 

################################################################################

####################################
#Connecting/creating Database
####################################
try:

        
    print("\nConnecting to the database ... \n")

    cnx = mysql.connector.connect(user=M_user, 
                                  password=M_password,
                                  host='localhost',
                                  db ='PurBeurre',
                                  auth_plugin='mysql_native_password')
        
    print("\nConnected successfully !\n")
    cursor = cnx.cursor()
        
        
except mysql.connector.Error as error:

    print("\nFailed to connect to the database : Database does not exist.\n")
    print("\nCreation of the database ...\n")
    
    cnx = mysql.connector.connect(user=M_user, 
                                  password=M_password,
                                  host='localhost',
                                  auth_plugin='mysql_native_password')

    
    try:
        cursor = cnx.cursor()
        execute_sql_from_file(cursor, "sql_script_purbeurre.sql")
        print("\nDatabase created with success !\n")
        
    except:
        
        print("Error while creating the database, thanks to contact the admin")

####################################
#Sorting data
####################################   


sorting_product("Yaourts")


####################################
#Closing Database connection
####################################

cursor.close()
cnx.close()


