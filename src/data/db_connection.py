import os
import psycopg2
from flask import g

class DBconnection:

    @staticmethod
    def connect():
        db_connection_dict = {
            'dbname': 'develop',
            'user': 'testuser',
            'password': 'pleaseletmein',
        }

        print("docker =", os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False))

        if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
            db_connection_dict['host'] = 'db'
        else:
            db_connection_dict['host'] = 'localhost'
            db_connection_dict['port'] = 5432

        global conn
        conn = psycopg2.connect(**db_connection_dict)
        # cur = conn.cursor()
        # cur.execute("SELECT name FROM filter_parameter")


# def get_db():

#     if 'db' not in g:
#         db_connection_dict = {
#             'dbname': 'develop',
#             'user': 'testuser',
#             'password': 'pleaseletmein',
#         }

#         print("docker =", os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False))

#         if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
#             db_connection_dict['host'] = 'db'
#         else:
#             db_connection_dict['host'] = 'localhost'
#             db_connection_dict['port'] = 5432

#         g.db = psycopg2.connect(**db_connection_dict) # connection

#     return g.db