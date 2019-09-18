#! /usr/bin/env python3
# coding: utf-8

# -tc- Mettre une docstring de module ici

import mysql.connector
# -tc- éviter les majuscules et les _ dans les noms de modules
from config import M_user,M_password

# -tc- Toujours créer des fonctions ou des classes pour avoir un meilleur 
# -tc- contrôle sur l'exécution. Simplification: jamais de code directement
# -tc- au niveau global du script
try:
    conn = mysql.connector.connect(host='localhost',
                                   user=M_user,
                                   password=M_password,
                                   auth_plugin='mysql_native_password')



    cursor = conn.cursor()

    # Delete record now
    # -tc- Attention, pas de majuscule dans les noms de variables!
    sql_Delete_query = """DROP database PurBeurre"""
    cursor.execute(sql_Delete_query)
    
    # Save (commit) the changes
    conn.commit()

    print("Database PurBeurre was Deleted successfully ")

except mysql.connector.Error as error:
    print("Failed to Delete Database: {}".format(error))

finally:
    # closing database connection.
    if (conn.is_connected()):
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
