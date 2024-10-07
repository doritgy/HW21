#1
"""
CREATE OR REPLACE FUNCTION hello_user(user_name varchar)
RETURNS varchar
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN CONCAT('hello  ', user_name, ' ', current_timestamp);
END;
$$;
select * from hello_user('Dorit')

hello  Dorit 2024-10-04 14:23:08.428013+03
"""
#2
"""
CREATE OR REPLACE FUNCTION arithmetic(_x double precision, _y double precision)
returns varchar

LANGUAGE plpgsql AS
$$
DECLARE
	a DOUBLE PRECISION := 0.0;
	b double precision := 0.0;
	c double precision := 1.0;
	d double precision := 1.0;

BEGIN
	a = _x + _y;
	b = _x - _y;
	c = _x * _y;
	d = _x / _y;

    RETURN CONCAT('addition  ', a, ' ','substruction   ', b ,' ', 'multiplication  ', c, ' ', 'division   ', d);
END;
$$;
select * from ARITHMETIC(3,5)

addition  8 substruction   -2 multiplication  15 division   0.6
"""

#3
"""
create or replace function minimum(_x integer, _y integer)
returns integer
LANGUAGE plpgsql AS
$$

BEGIN
	IF _x > _y THEN
        RETURN _y;
    ELSE
        RETURN _x;
    END IF;

END;
$$;
select * from minimum(20, 200)

minimum
20
"""
#4
"""
create or replace function min_three(_x integer, _y integer, _z integer)
returns integer
LANGUAGE plpgsql AS
$$

BEGIN
	IF _x < _y and _x < _Z THEN
        RETURN _x;
    ELSEif _y < _z then
        RETURN _y;
	ELSE
        RETURN _z;
    END IF;
END;
$$;
select * from min_three(20, 200, 2000)

min_three
20
"""
#5
"""
drop function randomize
CREATE OR REPLACE FUNCTION randomize(_x double precision, _y double precision)
returns double precision 

LANGUAGE plpgsql AS
$$
DECLARE
	rand  DOUBLE PRECISION := 0.0;
BEGIN
	rand = (random() * (_y - _x ) + _x);

    RETURN rand;
END;
$$;
select * from randomize(30 , 50)
randomize
47.83177646986978
"""
#6
"""
CREATE or replace function sp_books(
    OUT min_price double precision,
    OUT max_price double precision,
    OUT avg_price double precision,
	OUT count_books double precision)
language plpgsql AS
    $$
        BEGIN
            select min(price), max(price), avg(price)::numeric(5,2)
            into min_price, max_price, avg_price
            from books;
			select count(*) into count_books from books ;
        end;
    $$;

select * from sp_books();
min_p   max_p   avg_p   count
20.5	48.99	33.42	26.0
"""
#7a
"""
create or replace function sp_get_most_productive_writer(
out author_name text,
out num_books numeric)
language plpgsql AS
    $$
        BEGIN
     		select a.name, b.cnt_books into author_name, num_books
			from
				(select author_id, count(*) cnt_books from books
					group by author_id) b 
					join authors a on b.author_id = a.id
					where cnt_books = (select max(counted_books) from
					(select count(*) counted_books from books b 
					group by author_id));
        end
    $$;
select * from  sp_get_most_productive_writer()

J.R.R. Tolkien	4
"""
#7b
'''
drop function sp_get_less_productive_writer
CREATE OR REPLACE FUNCTION sp_get_less_productive_writer()
RETURNS TABLE (author_name TEXT, num_books bigint)
LANGUAGE plpgsql
AS $$
BEGIN

    RETURN QUERY
    SELECT a.name, b.min_count
    FROM (
        SELECT author_id, COUNT(*) AS min_count
        FROM books
        GROUP BY author_id
    ) b
    JOIN authors a ON b.author_id = a.id
    WHERE b.min_count = (
        SELECT MIN(counted)
        FROM (
            SELECT COUNT(*) AS counted
            FROM books
            GROUP BY author_id
        ));
END ;
	$$;
select * from sp_get_less_productive_writer()
Margaret Atwood	2
Mark Twain	2
Stephen King	2
Jane Austen	2
Isaac Asimov	2
'''
#8
"""
drop function sp_cheapest_book
create or replace function sp_cheapest_book(
out book_title text, out book_price double precision )
language plpgsql AS 
$$
	begin
	select b.title, b.price
	  into book_title, book_price
		from books b 
		where b.price = (select min(price) from books );

	end;
$$
select * from sp_cheapest_book()

The Adventures of Tom Sawyer	20.5
"""
#9
"""
create or replace function sp_avg_num_of_books(
out avg_num_of_books double precision)
language plpgsql AS 
$$
	begin
		--num_of_books = select count(*) from books;
		--num_of_authors = select count(*) from authors;
		--select (num_of_books + num_of_authors) / 2 into avg_num_of_books;
		select (select count(*) from books) + (select count(*) from authors) / 2
		into avg_num_of_books;
	end;
$$;
select * from sp_avg_num_of_books()
|avg_num_of_books|
|----------------|
|31              |
"""
#10
"""
CREATE OR REPLACE FUNCTION sp_insert_book(_title text, _release_date timestamp, _price double precision, _author_id bigint)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    new_id BIGINT := 0;
BEGIN
    INSERT INTO books (title, release_date, price, author_id)
    VALUES (_title, _release_date, _price, _author_id)
    RETURNING id INTO new_id;

    RETURN new_id; 
END;
$$;
select * from sp_insert_book('the good monther', '19980830 12:30', 32.60, 4)
|sp_insert_book|
|--------------|
|28            |
"""
#11
"""
CREATE OR REPLACE FUNCTION sp_insert_author(_title text, _release_date date, _price double precision, _author_name text)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    new_id BIGINT := 0;
BEGIN
    INSERT INTO authors (name)
      values(_author_name)
		RETURNING id INTO new_id;
    insert into books(title, release_date, price, author_id)
		values(_title, _release_date, _price, new_id);
    RETURN new_id; 
END;
$$;
select * from sp_insert_author('die with the wind','19581002', 80.20, 'bing crosby')
|sp_insert_author|
|----------------|
|12              |
"""
#12
"""
drop function sp_avg_books 
create or replace function sp_avg_books(out count_all_books bigint, out count_all_authors bigint, out avg_num_of_books numeric(5,2))
LANGUAGE plpgsql AS
	$$
 begin
	 	select count(*) into count_all_books from books; 
		select count(*) into count_all_authors from authors ;
		avg_num_of_books := count_all_books::numeric(5,2) / count_all_authors::numeric(5,2);
 end;
 $$
 select * from sp_avg_books()
 ||count_all_books|count_all_authors|avg_num_of_books|
|---------------|-----------------|----------------|
|28             |11               |2.5454545455    |

"""
#13
"""
create or replace procedure sp_update_book_details(_new_title text, _price double precision, _old_title text, _name text)
language plpgsql as
$$
begin 
	UPDATE books b
		SET title = _new_title, price = _price
		FROM authors a
		WHERE b.author_id = a.id
		  AND a.name like _name
		  AND b.title like _old_title;
end
$$
call sp_update_book_details('Harry Potter and the Philosophers Stone',50, 'Harry Potter and the thiefs', 'J.K. Rowling')

"""
#14
"""
create or replace procedure sp_update_author_details(_new_name text, _old_name text)
language plpgsql as
$$
begin 
	UPDATE authors a
		SET name = _new_name
		WHERE a.name like _old_name;
		 
end;
$$
call sp_update_author_details('J.K. Rolling', 'J.K. Rowling')
"""
#15
"""
drop function sp_get_books_in_range
create or replace function sp_get_books_in_range(_max_price double precision, _min_price double precision)
returns table(title text, price double precision)
language plpgsql as
$$
begin
	return query
	select b.title, b.price from books b
	where b.price between _min_price and _max_price;
end;
$$

select * from sp_get_books_in_range(45, 20)
|title                                   |price|
|----------------------------------------|-----|
|Harry Potter and the Chamber of Secrets |34.99|
|Harry Potter and the Prisoner of Azkaban|40.99|
|A Game of Thrones                       |45   |
|A Storm of Swords                       |42.99|
|The Hobbit                              |30.5 |

"""
#16
"""
CREATE OR REPLACE FUNCTION sp_get_exclusive_books(_first_author_name text, _second_author_name text)
RETURNS TABLE(title text, author_name text)
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY
    WITH books_auth1 AS (
        SELECT b.id FROM books b join authors a on b.author_id = a.id WHERE a.name like _first_author_name)
    , books_auth2 AS (
        SELECT b.id FROM  books b join authors a on b.author_id = a.id WHERE a.name like _second_author_name)
    
    SELECT b.title, a.name
    FROM books b JOIN authors a ON b.author_id = a.id
    WHERE b.id NOT IN (SELECT books_auth1.id FROM books_auth1)
    AND b.id NOT IN (SELECT books_auth2.id FROM books_auth2);
END;
$$;
select * from sp_get_exclusive_books('J.R.R. Tolkien', 'Agatha Christie' )

|title                                   |author_name       |
|----------------------------------------|------------------|
|Harry Potter and the Chamber of Secrets |J.K. Rolling      |
|Harry Potter and the Prisoner of Azkaban|J.K. Rolling      |
|A Game of Thrones                       |George R.R. Martin|
|A Clash of Kings                        |George R.R. Martin|
|A Storm of Swords                       |George R.R. Martin|
|Kafka on the Shore                      |Haruki Murakami   |
|Norwegian Wood                          |Haruki Murakami   |
|1Q84                                    |Haruki Murakami   |
|The Shining                             |Stephen King      |
|It                                      |Stephen King      |

"""
#17
"""
drop function sp_upsert_book
CREATE OR REPLACE FUNCTION sp_upsert_book(_title TEXT, _author_name text, _price double precision, _release_date date)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
    record_id BIGINT := 0;
	my_author_id bigint := 0;
BEGIN
    SELECT b.id INTO record_id 
    FROM books b join authors a on b.author_id = a.id  
    WHERE b.title like _title and a.name like _author_name ;

    IF NOT FOUND THEN
		select a.id into my_author_id from authors a where a.name = _author_name;
        INSERT INTO books (title, release_date, price, author_id)
        VALUES (_title, _release_date, _price, my_author_id)
        RETURNING id INTO record_id;
    ELSE
        UPDATE books 
        SET release_date = _release_date, price = _price
        WHERE books.id = record_id ; 
    END IF;

    RETURN record_id;  
END;
$$;
select * from sp_upsert_book('The sky is black', 'J.K. Rolling', 50.5, '20050830')


|id |title                                   |release_date|price|author_id|
|---|----------------------------------------|------------|-----|---------|
       |
|31 |The sky is blue                         |2005-08-30  |50.5 |         |
|32 |The sky is black                        |2005-08-30  |50.5 |1        |
here we can see two new records, when the query didn't find,
and I also checked that when he did find, then he changed the details

"""
#18
"""
CREATE OR REPLACE FUNCTION sp_book_details(_param1 TEXT)
RETURNS TABLE(id BIGINT, title TEXT, depends TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF _param1 = 'D' THEN
        RETURN QUERY
        SELECT b.id, b.title, b.release_date::TEXT AS depends
        FROM books b;
    ELSE
        RETURN QUERY
        SELECT b.id, b.title, a.name AS depends
        FROM books b JOIN authors a ON b.author_id = a.id;
    END IF;
END;
$$;
select * from sp_book_details('D)
with "D" in parameter
|id |title                                   |depends   |
|---|----------------------------------------|----------|
|3  |Harry Potter and the Prisoner of Azkaban|1999-07-08|
|4  |A Game of Thrones                       |1996-08-06|
|5  |A Clash of Kings                        |1998-11-16|
|6  |A Storm of Swords                       |2000-08-08|
|7  |The Hobbit                              |1937-09-21|
|8  |The Fellowship of the Ring              |1954-07-29|

select * from sp_book_details('E)
without 'D' in parameter
|id |title                                   |depends           |
|---|----------------------------------------|------------------|
|3  |Harry Potter and the Prisoner of Azkaban|J.K. Rolling      |
|4  |A Game of Thrones                       |George R.R. Martin|
|5  |A Clash of Kings                        |George R.R. Martin|
|6  |A Storm of Swords                       |George R.R. Martin|

"""
#19
"""
CREATE OR REPLACE FUNCTION sp_book_price(_paramb bool, _book_title text)
RETURNS double precision
LANGUAGE plpgsql
AS $$
declare
book_price numeric(5,2);
BEGIN
    IF _paramb  THEN
        SELECT b.price * 0.5::numeric(5,2) into book_price
        FROM books b
		where b.title like _book_title; 
    ELSE
        SELECT b.price::numeric(5,2) into book_price
        FROM books b
		where b.title like _book_title; 
    END IF;
	return book_price;
END;
$$;
select * from sp_book_price(FALSE,'The Hobbit')
|sp_book_price|
|-------------|
|30.5         |
select * from sp_book_price(TRUE,'The Hobbit')
|sp_book_price|
|-------------|
|15.25        |

"""
#19 BONUS1
"""
CREATE OR REPLACE FUNCTION sp_book_price_with_discount(_paramb bool, _book_title text, _disc numeric(5,2))
RETURNS numeric(5,2)
LANGUAGE plpgsql
AS $$
declare
book_price numeric(5,2);
BEGIN
    IF _paramb  THEN
        SELECT b.price * (100 -_disc) / 100 into book_price
        FROM books b
		where b.title like _book_title; 
    ELSE
        SELECT b.price into book_price
        FROM books b
		where b.title like _book_title; 
    END IF;
	return book_price;
END;
$$;
select * from sp_book_price_with_discount(TRUE,'The Hobbit', 10.50)
|sp_book_price_with_discount|
|---------------------------|
|27.3                       |

"""
#19 BONUS2
"""
CREATE OR REPLACE FUNCTION sp_book_price_with_discount2(_paramb BOOLEAN, _book_title TEXT, _disc NUMERIC(5,2))
RETURNS NUMERIC(5,2)
LANGUAGE plpgsql
AS $$
DECLARE
    book_price NUMERIC(5,2);
BEGIN
    IF _paramb THEN
        -- Apply discount when _paramb is TRUE
        SELECT b.price * (100 - _disc) / 100 INTO book_price
        FROM books b
        WHERE b.title ILIKE _book_title;
    ELSIF _disc <> 0 THEN
        -- Log a warning but return the genuine price
        RAISE WARNING 'Discount provided, but _paramb is FALSE. Returning original price.';
        SELECT b.price INTO book_price
        FROM books b
        WHERE b.title ILIKE _book_title;
    ELSE
        -- Return the genuine price when no discount is applied and _paramb is FALSE
        SELECT b.price INTO book_price
        FROM books b
        WHERE b.title ILIKE _book_title;
    END IF;
    
    RETURN book_price;
END;
$$;
select * from sp_book_price_with_discount2(FALSE, 'THE Hobbit', 50)
|sp_book_price_with_discount2|
|----------------------------|
|30.5                        |

output:
FALSE WITH DISCOUNT, ANSWER INCLUDES GENUINE PRICENT
Discount provided, but _paramb is FALSE. Returning original price.
"""
#20
"""
CREATE OR REPLACE FUNCTION sp_get_book_loop(_book_title TEXT)
RETURNS BIGINT
LANGUAGE plpgsql AS
$$
DECLARE
   book_index BIGINT := 0;
   book_title_found TEXT;
   max_id BIGINT;
BEGIN
	SELECT MAX(id) INTO max_id FROM books;
    FOR i IN 1..max_id LOOP 
		SELECT b.title INTO book_title_found FROM books b WHERE b.id = i;
		IF book_title_found IS NOT NULL AND book_title_found = _book_title THEN
            book_index := i;
            EXIT; 
        END IF;
    END LOOP;
    
    RETURN book_index;
END;
$$;
select * from sp_get_book_loop('The Hobbit')
|sp_get_book_loop|
|----------------|
|7               |

"""






