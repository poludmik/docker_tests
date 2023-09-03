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


    # Get db version
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(f'PostgreSQL database version: {db_version}')
    print()


    # Select all users
    cur.execute("select * from user_account where first_name = 'Egor' limit 1")
    for record in cur:
        print(record)


    # Select IDs and usernames of all users with first name of length "first_name_len" AT ONCE
    cur.execute("SELECT date_of_birth, username FROM user_account WHERE length(first_name)=%s AND last_name=%s", (4, "Menshikov"))
    print("\n", cur.fetchall())


    # Delete row
    prefix_to_delete = 'hungry_joakimbroden'
    cur.execute(f"DELETE FROM username_prefix WHERE prefix = '{prefix_to_delete}'")


    # Insert row
    prefix_to_insert = 'hungry_mccartney'
    cur.execute(f"INSERT INTO username_prefix (prefix) VALUES ('{prefix_to_insert}') ON CONFLICT (prefix) DO NOTHING;")


    # Insert and update row
    values = ('afb73dd5-f1de-4b37-86cc-9e177b04c7db', 
              '2024-01-01', 
              'kek@mydlo.com', 
              'Kolya', 
              '$2a$10$5sLlVP8g6pW9GGx3eyw7I.KjosvIXfD.z1pZ2eHyrt8MTN16oN5PW', 
              'Denisov', 
              'USER', 
              '2020-01-21 18:14:00.111111', 
              'kek',
              )
    cur.execute(f"DELETE FROM user_account WHERE username = 'kek'") # delete if existed...
    cur.execute("INSERT INTO user_account VALUES %s", (values, ))
    cur.execute(f"UPDATE user_account SET email = 'oPrivet@kolya.com' WHERE username = 'kek'")


    # Close cursor
    cur.close()

    # Commit db: save DELETEs and INSERTs
    conn.commit()

    # don't forget to close the connection too!!!!!!
    # >:)
    conn.close()
