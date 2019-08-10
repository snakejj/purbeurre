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
        
        cursor.execute(command)
    

def filling_category_db(cursor):
    

    
    cursor.execute("""SELECT * FROM Category""")

    rows_count = cursor.fetchone()

    if rows_count == None:
        try:
            
            cursor.execute("""INSERT INTO Category (category_name)
                              VALUES
                              ('Yaourts'),
                              ('Chocolats'),
                              ('Boissons'),
                              ('Snacks'),
                              ('Produits laitiers');""")
            
                
            print("Categories successfully inserted !")
            cnx.commit()
            
        except:
            
            print("Error while inserting categories in DB")
    else:
        print("Categories already in the DB")

    
def sorting_product(cursor,category):

    
    
    response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms2={}&action=process&json=1&page_size=20".format(category))
    result = json.loads(response.text)

    cursor.execute('SELECT category_id FROM Category WHERE category_name = (%s)', (category,))
    numid = cursor.fetchone()
    print(numid)

    for p in result['products'] :
        if p['code'] and p['product_name_fr'] and p['url'] and p['stores'] and p['ingredients_text_fr'] and p['nutrition_grades_tags']:

            cursor.execute("INSERT INTO Food VALUES (%s, %s, %s, %s, %s, %s, %s)", (p['code'], numid, p['product_name_fr'], p['ingredients_text_fr'], p['stores'], p['url'], p['nutrition_grades_tags'], ))
            cnx.commit()
        else:
            print("Incomplet !") 
        


    

#def filling_product_db():

    

################################################################################

####################################
#Connecting/creating Database
####################################

connected = True


try:
    
        
    print("\nConnecting to the database ... \n")

    cnx = mysql.connector.connect(user=M_user, 
                                  password=M_password,
                                  host='localhost',
                                  db ='PurBeurre',
                                  auth_plugin='mysql_native_password')
        
    print("\nConnected successfully !\n")
    
    cursor = cnx.cursor()
    print("\nOuverture du cursor !\n")
    
        
        
except mysql.connector.Error as error:

    print("\nFailed to connect to the database : Database does not exist.\n")
    print("\nCreation of the database ...\n")
    
    cnx = mysql.connector.connect(user=M_user, 
                                  password=M_password,
                                  host='localhost',
                                  auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    print("\nOuverture du cursor lors du else !\n")
    
    try:
        
        execute_sql_from_file(cursor, "sql_script_purbeurre.sql")
        print("\nDatabase created with success !\n")
        
    except:
        
        print("Error while creating the database, thanks to contact the admin")
        cursor.execute("DROP database PurBeurre;")             
        connected = False
        

####################################
# MAIN
####################################   


if connected :
    filling_category_db(cursor)
    toto = "TOTO"
    titi = "tadsrata"
    idnumo = 2
#    cursor.execute("INSERT INTO Category (category_name) VALUES (%s)", (toto, )) 
    cursor.execute('UPDATE Category SET category_name= (%s) WHERE category_id = (%s)', (titi, idnumo,))
    cnx.commit()
    sorting_product(cursor, "Boissons")

#    sorting_product(cursor,"Yaourts")
    
    # TEST VARIABLE IN SQL QUERY.
   
#    sql_test_query = """UPDATE Category SET category_name= %s where id = %s""", ("TOTO", 3
    
    
#    cursor.execute(sql_test_query)

#    cnx.commit()
#    cursor.close()
    # FIN TEST VARIABLE 





