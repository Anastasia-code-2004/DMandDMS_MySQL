SELECT user_id, email, is_superuser
FROM "user";


SELECT email
FROM "user"
WHERE is_superuser = TRUE;


SELECT movie_id, title, poster, description, duration, release_date, rating
FROM movie
ORDER BY release_date DESC;


SELECT movie_id, title, poster, description, duration, release_date, rating 
FROM movie
WHERE title ILIKE '%на%';


SELECT title, rating, release_date
FROM movie
WHERE rating > 8
ORDER BY rating DESC;


SELECT title, release_date, poster
FROM movie
WHERE release_date > '2023-01-01'
ORDER BY release_date;

SELECT title, duration, poster
FROM movie
WHERE duration > 120
ORDER BY duration DESC;


SELECT name
FROM genre
ORDER BY name;

SELECT genre_id, COUNT(movie_id) FROM movie_genres GROUP BY genre_id;


SELECT description, rating, date,
       (SELECT email FROM "user" WHERE review.user_id = "user".user_id)
FROM review;


SELECT description, rating, date,
       (SELECT email FROM "user" WHERE review.user_id = "user".user_id)
FROM review
WHERE movie_id = (
    SELECT movie_id 
    FROM movie 
    WHERE title = 'Дюна'
);


SELECT (SELECT title FROM movie WHERE movie.movie_id = showtime.movie_id),
       (SELECT poster FROM movie WHERE movie.movie_id = showtime.movie_id),
       (SELECT name FROM hall WHERE hall.hall_id = showtime.hall_id),
       start_time, 
       end_time,
       price 
FROM showtime
ORDER BY start_time;


SELECT start_time, end_time, price
FROM showtime
WHERE movie_id = (
    SELECT movie_id 
    FROM movie 
    WHERE title = 'Бэтмен'
);


SELECT hall_id, name
FROM hall;


SELECT hall_id, MIN(price) FROM showtime GROUP BY hall_id;


SELECT seat_id, row, number
FROM seat
WHERE hall_id = 5
ORDER BY row, number;


SELECT purchase_date, 
       (SELECT start_time FROM showtime WHERE ticket.showtime_id = showtime.showtime_id),
       (SELECT row FROM seat WHERE ticket.seat_id = seat.seat_id),
       (SELECT number FROM seat WHERE ticket.seat_id = seat.seat_id)
FROM ticket
WHERE user_id = 12;


SELECT title
FROM movie
WHERE movie_id IN (
    SELECT movie_id
    FROM movie_genres
    WHERE genre_id = (
        SELECT genre_id
        FROM genre
        WHERE name = 'Драма'
    )
);


SELECT action_type, date
FROM user_action_log
WHERE user_id = 11
ORDER BY date DESC;


SELECT showtime_id, COUNT(ticket_id) AS ticket_count
FROM ticket
GROUP BY showtime_id;


SELECT genre_id, COUNT(movie_id) AS movie_count
FROM movie_genres
WHERE genre_id IN (6, 7, 8)
GROUP BY genre_id
ORDER BY genre_id;
