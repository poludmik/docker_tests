import numpy as np
import psycopg2


if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        # url=,
        # database="postgresql",
        user="testuser",
        password="pleaseletmein",
        port=5432,
        )

    cur = conn.cursor()
	# execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    cur.close()


    # while(True):
    #     print("where number")
    #     n = int(input())
    #     print(np.random.rand(1, n))

