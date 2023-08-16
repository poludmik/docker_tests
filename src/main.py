import sys
import numpy as np
import psycopg2

if __name__ == "__main__":
    db_connection_dict = {
        'dbname': 'develop',
        'user': 'testuser',
        'password': 'pleaseletmein',
    }

    if len(sys.argv) == 2 and sys.argv[1] == '-docker':
        # this script was run from docker
        db_connection_dict['host'] = 'db'
        pass
    else:
        # this script was run locally
        db_connection_dict['host'] = 'localhost'
        db_connection_dict['port'] = 5432
        pass

    conn = psycopg2.connect(**db_connection_dict)
    cur = conn.cursor()

    # db version
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(f'PostgreSQL database version: {db_version}')
    print()

    # retrieve all users ONE BY ONE
    cur.execute('SELECT * FROM user_account')
    print('All users:')
    for record in cur:
        print(record)
    print()

    # retrieve IDs and usernames of all users with first name of length "first_name_len" AT ONCE
    first_name_len = 4
    cur.execute('SELECT acc.id, acc.username FROM user_account acc WHERE length(acc.first_name)=%s', (first_name_len,))
    # equals to cur.execute('SELECT acc.id, acc.username FROM user_account acc WHERE length(acc.first_name)=4')
    print(f'Users with first name of length {first_name_len}:')
    print(cur.fetchall())

    cur.close()

    # don't forget to close the connection too!!!!!!
    conn.close()

    # while(True):
    #     print("where number")
    #     n = int(input())
    #     print(np.random.rand(1, n))
