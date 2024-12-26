CREATE OR REPLACE PROCEDURE booking_ticket(
    IN user_id INT,
    IN showtime_id INT,
    IN seat_id INT
)
AS
$$
BEGIN
    -- Вставляем билет и получаем его ID с помощью RETURNING
    BEGIN
        INSERT INTO ticket (user_id, showtime_id, seat_id, purchase_date)
		VALUES (user_id, showtime_id, seat_id, NOW());
 
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'Не удалось забронировать билет. Ошибка: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;

DROP PROCEDURE booking_ticket(integer,integer,integer);

CREATE OR REPLACE FUNCTION get_seats_for_showtime(showtime_id INT)
RETURNS TABLE (
    "row" SMALLINT,
    seat_number SMALLINT,
    is_available BOOLEAN
)
AS
$$
BEGIN
    RETURN QUERY
    SELECT
        s.row,
        s.number AS seat_number,
        CASE 
            WHEN t.seat_id IS NULL THEN TRUE  -- Место свободно
            ELSE FALSE -- Место занято
        END as is_available
    FROM
        seat s
    JOIN
        showtime st ON st.hall_id = s.hall_id AND st.showtime_id = $1
    LEFT JOIN
        ticket t ON t.seat_id = s.seat_id AND t.showtime_id = $1;  -- Проверяем, 
											-- забронировано ли место
END;
$$ LANGUAGE plpgsql;

select * from showtime;
select * from get_seats_for_showtime(4);


CREATE OR REPLACE PROCEDURE create_movie_with_genres(
    p_title VARCHAR(255), 
    p_description TEXT, 
    p_duration INT, 
    p_release_date DATE, 
    p_genre_ids INT[]  -- Массив идентификаторов жанров
)
AS
$$
DECLARE
    p_movie_id INT;
    i INT;
BEGIN
    -- Вставляем новый фильм в таблицу movie
    INSERT INTO movie (title, description, duration, release_date)
    VALUES (p_title, p_description, p_duration, p_release_date)
    RETURNING movie_id INTO p_movie_id;

    -- Связываем фильм с жанрами из массива p_genre_ids
    FOREACH i IN ARRAY p_genre_ids LOOP
        -- Добавляем связь между фильмом и жанром
        INSERT INTO movie_genres (movie_id, genre_id)
        VALUES (p_movie_id, i);
    END LOOP;

    RAISE NOTICE 'Фильм с ID % был успешно создан и связан с жанрами.', p_movie_id;
END;
$$ LANGUAGE plpgsql;

select * from genre;
CALL create_movie_with_genres(
    'Назад в будущее', 
    'Путешествие во времени...', 
    116, 
    '1985-07-03', 
    ARRAY[6, 7]  
);

CREATE OR REPLACE PROCEDURE delete_old_showtimes()
as
$$
begin
	delete from showtime where end_time < NOW();
end;
$$ language plpgsql;


CREATE OR REPLACE PROCEDURE register_user(
    p_email TEXT,
    p_password TEXT,
    p_is_active BOOLEAN DEFAULT TRUE,
    p_is_staff BOOLEAN DEFAULT FALSE,
    p_is_superuser BOOLEAN DEFAULT FALSE
)
AS 
$$
DECLARE
    user_id INT;
BEGIN
    -- Вставляем данные о пользователе в таблицу users
    INSERT INTO users (email, password, is_active, is_staff, is_superuser, date_joined)
    VALUES (p_email, crypt(p_password, gen_salt('bf')), p_is_active, p_is_staff, p_is_superuser, NOW())
    RETURNING user_id INTO user_id;
    
    -- Можно вернуть id нового пользователя, если это нужно
    RAISE NOTICE 'New user created with id: %', user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE create_showtime(
    p_movie_id INT, 
    p_hall_id INT, 
    p_start_time TIMESTAMP, 
    p_price DECIMAL(6, 2)
)
AS
$$
BEGIN
    INSERT INTO showtime (movie_id, hall_id, start_time, price)
    VALUES (p_movie_id, p_hall_id, p_start_time, p_price);
	EXCEPTION
        WHEN OTHERS THEN -- условие перехваа всех ошибок
			-- Команда для вывода сообщения
            RAISE NOTICE 'Не удалось сформировать сеанс. Ошибка: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


select * from showtime;
call create_showtime(7, 5, '2024-12-31 14:00:00', 18);

CREATE OR REPLACE PROCEDURE add_review(
	p_user_id INT, 
    p_movie_id INT, 
    p_description TEXT, 
    p_rating SMALLINT
)
AS
$$
begin
	INSERT INTO review (user_id, movie_id, description, rating)
    VALUES (p_user_id, p_movie_id, p_description, p_rating);
	EXCEPTION
		WHEN OTHERS THEN
			RAISE NOTICE 'Не удалось оставить отзыв. Ошибка: %', SQLERRM;
end;
$$ language plpgsql;


CREATE OR REPLACE PROCEDURE create_hall_and_seats(
    p_hall_name VARCHAR(255), 
    p_rows INT, 
    p_seats_per_row INT
)
AS
$$
DECLARE
    p_hall_id INT;
    i INT;
    j INT;
BEGIN
    -- Создаем новый зал
    INSERT INTO hall (name) 
    VALUES (p_hall_name)
    RETURNING hall_id INTO p_hall_id;

    -- Добавляем места в зал
    FOR i IN 1..p_rows LOOP
        FOR j IN 1..p_seats_per_row LOOP
            INSERT INTO seat (hall_id, row, number)
            VALUES (p_hall_id, i, j);
        END LOOP;
    END LOOP;

    RAISE NOTICE 'Зал "%" с % рядами и % местами в каждом ряду успешно создан!', p_hall_name, p_rows, p_seats_per_row;
END;
$$ LANGUAGE plpgsql;

call create_hall_and_seats('Зал повышенного комфорта', 5, 5);

select * from hall;
select * from seat where hall_id = 7;

CREATE OR REPLACE FUNCTION get_showtimes(input_date TIMESTAMP DEFAULT NULL)
RETURNS TABLE (
    date TIMESTAMP,
    title VARCHAR(255),
    hall_name VARCHAR(255),
    price DECIMAL(6, 2)
)
AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        s.start_time AS date,
        m.title,
        h.name AS hall_name,
        s.price
    FROM 
        showtime s
    JOIN 
        movie m ON s.movie_id = m.movie_id
    JOIN 
        hall h ON s.hall_id = h.hall_id
    WHERE 
        input_date IS NULL OR DATE(s.start_time) = DATE(input_date);

END;
$$ LANGUAGE plpgsql;

select * from get_showtimes('2024-12-31 14:00:00');


 SELECT 
                t.purchase_date AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow' AS purchase_date, 
                sh.price, 
                sh.start_time AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow' AS start_time, 
                h.name, 
                s.row, 
                s.number, 
                m.title
            FROM ticket t
            JOIN showtime sh ON sh.showtime_id = t.showtime_id
            JOIN seat s ON s.seat_id = t.seat_id
            JOIN "user" u ON u.user_id = t.user_id
            JOIN hall h ON h.hall_id = sh.hall_id
            JOIN movie m ON m.movie_id = sh.movie_id
            WHERE t.user_id = 20;



SET timezone = 'Europe/Minsk';

SELECT * FROM review;
SHOW timezone;

SELECT NOW();


SELECT purchase_date AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow'
FROM ticket;

ALTER TABLE ticket
ALTER COLUMN purchase_date TYPE TIMESTAMP;
ALTER COLUMN purchase_date SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE review
ALTER COLUMN date TYPE TIMESTAMP WITH TIME ZONE;

ALTER TABLE review
ALTER COLUMN date SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE user_action_log
ALTER COLUMN date TYPE TIMESTAMP;

ALTER TABLE user_action_log
ALTER COLUMN date SET DEFAULT CURRENT_TIMESTAMP;

select * from ticket;
select * from review;


ALTER DATABASE "Cinema" SET timezone = 'Europe/Moscow';

SHOW timezone;

-- Изменение столбца на тип timestamp with time zone
-- Изменение столбца на тип timestamp with time zone
ALTER TABLE ticket
  ALTER COLUMN purchase_date SET DATA TYPE TIMESTAMP WITH TIME ZONE;

SHOW timezone;

delete from ticket where user_id = 20;

select * from ticket;

