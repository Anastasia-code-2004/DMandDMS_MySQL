ALTER TABLE movie
ALTER COLUMN poster TYPE VARCHAR(255);

INSERT INTO "user" (email, password, is_superuser)
VALUES ('adminCinemaMiracle@gmail.com', 'Enabledtrue', TRUE);

INSERT INTO "user" (email, password, is_superuser)
VALUES ('anastasinikolaychik@gmail.com', 'Ttesting1', FALSE);

INSERT INTO "user" (email, password, is_superuser) 
VALUES ('alice@gmail.com', 'alice_secure_password', FALSE);

INSERT INTO "user" (email, password, is_superuser) 
VALUES ('bob@mail.ru', 'bob_safe_password', FALSE);

INSERT INTO "user" (email, password, is_superuser)
VALUES ('lizamalina73@gmail.com', 'Ilovemalina18', FALSE);

INSERT INTO "user" (email, password, is_superuser)
VALUES ('nicolaichik2018@yandex.by', 'Ttesting1', FALSE);


INSERT INTO movie (title, description, duration, poster, release_date, rating)
VALUES (
    'Дюна',
    'Фантастический эпос о молодой благородной семье, которая борется за контроль над пустынной планетой Арракис, источником ценнейшего ресурса во Вселенной.',
    155,
    NULL, 
    '2021-10-22',
    8.1
);

INSERT INTO movie (title, description, duration, poster, release_date, rating)
VALUES (
    'Не смотрите наверх',
    'Чёрная комедия о двух астрономах, которые обнаруживают огромную комету, движущуюся к Земле. Они пытаются предупредить мир, но сталкиваются с недоверием и безразличием.',
    138,
    NULL,  
    '2021-12-24',
    7.2
);

INSERT INTO movie (title, description, duration, poster, release_date, rating)
VALUES (
    'Бэтмен',
    'Темная, мрачная история о Брюсе Уэйне, который борется с преступностью в Готэме как Бэтмен, сталкиваясь с загадочным злодеем Загадочником.',
    176,
    NULL,  
    '2022-03-04',
    7.9
);

INSERT INTO movie (title, description, duration, poster, release_date, rating)
VALUES (
    'Опенгеймер',
    'Биографическая драма о жизни Роберта Оппенгеймера, ключевого физика, который сыграл главную роль в разработке атомной бомбы во время Второй мировой войны.',
    180,
    NULL, 
    '2023-07-21',
    8.8
);

INSERT INTO movie (title, description, duration, poster, release_date, rating)
VALUES (
    'Миссия невыполнима: Смертельная расплата. Часть первая',
    'Этан Хант и его команда снова берутся за выполнение почти невыполнимой миссии, где ставки высоки, а предательство повсюду.',
    163,
    NULL,  
    '2023-07-12',
    7.9
);


INSERT INTO genre (name, description)
VALUES 
('Фантастика', 'Жанр, включающий элементы вымышленного мира, науки будущего и технологий.'),
('Драма', 'Фильмы, сосредоточенные на эмоциональных и психологических конфликтах.'),
('Комедия', 'Фильмы, предназначенные вызвать смех и поднять настроение.'),
('Ужасы', 'Жанр, целью которого является создание у зрителя чувства страха, напряжения и тревоги.'),
('Приключения', 'Фильмы, полные захватывающих событий, путешествий и опасностей.');



INSERT INTO movie_genres (movie_id, genre_id)
VALUES
(1, 1),
(1, 2),
(2, 3), 
(2, 2),
(3, 1), 
(3, 2),
(3, 5),
(4, 2),
(5, 1),
(5, 2), 
(5, 5);



INSERT INTO hall (name)
VALUES ('Зал 1'), ('Зал 2'), ('Зал 3');

DO $$
DECLARE
    i INT;  
BEGIN
    FOR i IN 1..20 LOOP
        INSERT INTO seat (hall_id, row, number)
        VALUES (1, (i - 1) / 10 + 1, (i - 1) % 10 + 1);  
    END LOOP;
END $$;


DO $$
DECLARE
    i INT;  
BEGIN
    FOR i IN 1..10 LOOP
        INSERT INTO seat (hall_id, row, number)
        VALUES (2, (i - 1) / 5 + 1, (i - 1) % 5 + 1);  
    END LOOP;
END $$;

INSERT INTO seat (hall_id, row, number)
VALUES 
(3, 1, 1),
(3, 1, 2),
(3, 2, 1),
(3, 2, 2),
(3, 2, 3);



INSERT INTO showtime (movie_id, hall_id, start_time, end_time, price)
VALUES
(1, 1, '2024-10-17 14:00:00', '2024-10-17 16:30:00', 15.00),  
(2, 2, '2024-10-17 17:00:00', '2024-10-17 19:15:00', 23.00),  
(3, 3, '2024-10-17 20:00:00', '2024-10-17 22:45:00', 40.00);



INSERT INTO ticket (user_id, showtime_id, seat_id)
VALUES
(2, 1, 1),  
(2, 1, 2),  
(3, 2, 21),
(4, 2, 22), 
(5, 3, 33);



INSERT INTO review (user_id, movie_id, description, rating)
VALUES
(2, 1, 'Очень захватывающий фильм с потрясающими спецэффектами и сюжетом.', 9),  
(2, 2, 'Интересная история, но немного затянуто.', 7), 
(3, 1, 'Фильм отличный, но не понравилась концовка.', 8),  
(4, 3, 'Отличный саундтрек и визуальные эффекты, но сюжет слабоват.', 6), 
(5, 2, 'Прекрасная актёрская игра, рекомендую к просмотру.', 9);



INSERT INTO user_action_log (user_id, date, action_type)
SELECT user_id, date, 'Написан отзыв' FROM review
UNION
SELECT user_id, purchase_date, 'Куплен билет' FROM ticket
UNION
SELECT user_id, CURRENT_TIMESTAMP, 'Зарегистрирован пользователь' FROM "user";
