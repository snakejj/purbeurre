#! /usr/bin/env python3
# coding: utf-8

""" """

import mysql.connector

from config import USER, PASSWORD



def main():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password'
        )

        cursor = conn.cursor()

        # Delete record now

        sql_delete_query = """DROP database PurBeurre"""
        cursor.execute(sql_delete_query)

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


if __name__ == "__main__":
    main()
