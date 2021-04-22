import psycopg2

# Create postgres table
def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL
        )
        """)
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname="your-db-name", host="host",
                             user="user", password="pass", sslmode='require')
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
