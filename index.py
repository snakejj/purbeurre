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
            cnx.commit()
            
        except:
            
            print("Error while inserting categories in DB")
    else:
        print("Categories already in the DB !")

    
def sorting_and_filling_product(cursor,category):

    
    
    response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms2={}&action=process&json=1&page_size=100".format(category))
    result = json.loads(response.text)

#    cursor.execute('SELECT food_id FROM Food WHERE category_id = 2')
#    rows_count = cursor.fetchall()
#    print(rows_count)

#    if not rows_count:
#        try:
#            print("Row count est vide")
    cursor.execute('SELECT category_id FROM Category WHERE category_name = (%s)', (category,))
    numid = cursor.fetchone()
    #    print(numid[0])
    for p in result['products'] :
        if p['code'] and 4 < len(p['product_name_fr']) < 80 and len(p['url']) < 255 and 1 < len(p['stores']) < 150 and p['ingredients_text_fr'] and len(p['nutrition_grades_tags'][0]) == 1:
            
#            print(p['nutrition_grades_tags'][0])
#            print(p['stores'])
            cursor.execute("INSERT INTO Food (category_id, food_name, ingredients_text, store, off_link, nutriscore) VALUES (%s, %s, %s, %s, %s, %s)", (numid[0], p['product_name_fr'], p['ingredients_text_fr'], p['stores'], p['url'], p['nutrition_grades_tags'][0], ))
            

                    
            cnx.commit()
#        except:
            
#            print("EROOOOR") 
     
#    else :
#            print("else")       
    
        
#        else:
#            print("Incomplet !") 
        

def categ_select():

    cursor.execute('SELECT * FROM Category')
    result = cursor.fetchall()
    for a,b in result:
        print(a,":",b)
    menu_choice = int(input("Enter le numéro de la categorie souhaité : "))
    
    while menu_choice < 1 or menu_choice > 5 :
        
        menu_choice = int(input("Enter le numéro de la categorie souhaité : "))              

    else :

        product_select(menu_choice)
        

def product_select(numcateg):

    cursor.execute('SELECT food_id, food_name FROM Food WHERE category_id = (%s)', (numcateg,))
    result = cursor.fetchall()
    for a,b in result:
        print(a,":",b)
    pass


    

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
        
    print("Connected successfully !\n")
    
    cursor = cnx.cursor()
#    print("Cursor opening !\n")
    
        
        
except mysql.connector.Error as error:

    print("Failed to connect to the database : Database does not exist.\n")
    print("Creation of the database ...\n")
    
    cnx = mysql.connector.connect(user=M_user, 
                                  password=M_password,
                                  host='localhost',
                                  auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
#    print("Cursor opening in else !\n")
    
    try:
        
        execute_sql_from_file(cursor, "sql_script_purbeurre.sql")
        print("Database created with success !\n")
        
    except:
        
        print("Error while creating the database, thanks to contact the admin")
        cursor.execute("DROP database PurBeurre;")             
        connected = False
        

####################################
# MAIN
####################################   


if connected :
    filling_category_db(cursor)
    sorting_and_filling_product(cursor, "Yaourts")
    sorting_and_filling_product(cursor, "Chocolats")
    sorting_and_filling_product(cursor, "Boissons")
    sorting_and_filling_product(cursor, "Snacks")
    sorting_and_filling_product(cursor, "Produits laitiers")


####################################
# TERMINAL INTERFACE
####################################  

print("""

##############################################################

      """)

ongoing = True



print("1 - Quel aliment souhaitez-vous remplacer ?")
print("2 - Retrouver mes aliments substitués.")
print("3 - Quitter !")
    
menu_choice = int(input("Enter le numéro de l'option souhaité : "))

while menu_choice < 1 or menu_choice > 3 :
    menu_choice = int(input("Enter le numéro de l'option souhaité : "))
    
if menu_choice == 1 :
        
    categ_select()
              

elif menu_choice == 2 :

    print("En cours de dev")
        

elif menu_choice == 3 :
    print("Au revoir")
    

    
    



