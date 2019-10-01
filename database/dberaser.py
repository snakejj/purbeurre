#! /usr/bin/env python3
# coding: utf-8

""" Module which allows to erase the database """

import mysql.connector

from configdb import USER, PASSWORD, HOST, DB_NAME, AUTH_PLUGIN, PORT


def main():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin=AUTH_PLUGIN,
            port=PORT
        )

        cursor = conn.cursor()

        # Delete record now

        sql_delete_query = "DROP database %s" % DB_NAME
        cursor.execute(sql_delete_query)

        # Save (commit) the changes
        conn.commit()

        print(
            "La base de données",
            DB_NAME,
            "a été effacée avec succées.")

    except mysql.connector.Error:
        print(
            "Impossible d'effacer la base de données",
            DB_NAME,
            "car elle n'existe pas."
            )

    finally:
        # closing database connection.
        if (conn.is_connected()):
            cursor.close()
            conn.close()


if __name__ == "__main__":
    main()
