import psycopg2
import psycopg2.extras

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",  # postgres
    password="admin",
    port="5559"
)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
insert_query = """insert into books (title, release_date, price, author_id)
values (%s, %s, %s, %s) returning id;
"""
insert_values = ('The good mother', '2020-07-30', 59, 3)
cursor.execute(insert_query, insert_values)
new_id = cursor.fetchone()[0]
print('new_id', new_id)

connection.commit()

cursor.close()
connection.close()

##new_id 33