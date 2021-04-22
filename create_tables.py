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
        conn = psycopg2.connect(dbname="d9p0qicl7pm3vq", host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
                             user="lokvtsuxecycfi", password="bf7217b8d02ceac97a86dd48d5f6a3d3e68fceb7917f22e82eb422157b240a90", sslmode='require')
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