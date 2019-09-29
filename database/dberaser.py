#! /usr/bin/env python3
# coding: utf-8

""" Module which allows to erase the database """

import mysql.connector

from configdb import USER, PASSWORD


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

        print("La base de données PurBeurre a été effacée avec succées ")

    except mysql.connector.Error:
        print("Impossible d'effacer la base de données car elle n'existe pas")

    finally:
        # closing database connection.
        if (conn.is_connected()):
            cursor.close()
            conn.close()


if __name__ == "__main__":
    main()
