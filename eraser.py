#! /usr/bin/env python3
# coding: utf-8

import mysql.connector
from config import M_user,M_password


try:
    conn = mysql.connector.connect(host='localhost',
                                   user=M_user,
                                   password=M_password,
                                   auth_plugin='mysql_native_password')



    cursor = conn.cursor()

    # Delete record now
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
