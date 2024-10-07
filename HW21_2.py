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
select_query = " SELECT * from sp_get_less_productive_writer()"

cursor.execute(select_query)

rows = cursor.fetchall()
print(rows)
for row in rows:
    rows_dict = dict(row)
    print(rows_dict)
    print(f"NAME: {row['author_name']} min_count: {row['num_books']:^20}")

##NAME: bing crosby min_count:      1
#####################################
select_query = " SELECT * from sp_get_most_productive_writer()"
cursor.execute(select_query)
rows = cursor.fetchall()
print(rows)
for row in rows:
    rows_dict = dict(row)
    print(rows_dict)
    print(f"NAME: {row['author_name']} min_count: {row['num_books']:^20}")

##NAME: J.R.R. Tolkien min_count:          4
######################################
select_query = "select * from sp_cheapest_book()"
cursor.execute(select_query)
rows = cursor.fetchall()
print(rows)
for row in rows:
    rows_dict = dict(row)
    print(rows_dict)
    print(f"TITLE: {row['book_title']} PRICE: {row['book_price']:^20}")

##TITLE: The Adventures of Tom Sawyer PRICE:         20.5

cursor.close()
connection.close()