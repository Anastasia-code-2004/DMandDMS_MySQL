SELECT m.title AS movie_title, g.name AS genre_name
FROM movie AS m
INNER JOIN movie_genres AS mg ON m.movie_id = mg.movie_id
INNER JOIN genre AS g ON mg.genre_id = g.genre_id;


SELECT email, m.title, r.description, r.rating
FROM "user"
LEFT JOIN review AS r ON r.user_id = "user".user_id
LEFT JOIN movie AS m ON m.movie_id = r.movie_id;


SELECT "name" AS genre, title AS movie
FROM genre AS g
JOIN movie_genres AS mg ON g.genre_id = mg.genre_id
RIGHT JOIN movie AS m ON m.movie_id = mg.movie_id;


SELECT h.name, s.row, s.number, t.ticket_id
FROM ticket AS t
RIGHT JOIN seat AS s ON t.seat_id = s.seat_id AND t.showtime_id = 4
JOIN hall AS h ON h.hall_id = s.hall_id
WHERE h.hall_id = (SELECT hall_id FROM showtime WHERE showtime_id = 4);


explain analyze SELECT "user".user_id, email, logs.date, logs.action_type
FROM "user"
FULL OUTER JOIN user_action_log AS logs ON "user".user_id = logs.user_id;


explain analyze SELECT "user".user_id, email, logs.date, logs.action_type
FROM "user"
LEFT JOIN user_action_log AS logs ON logs.user_id = "user".user_id

UNION

SELECT "user".user_id, email, logs.date, logs.action_type
FROM "user"
RIGHT JOIN user_action_log AS logs ON logs.user_id = "user".user_id;


SELECT movie.title, hall.name, '2024-11-01 14:00:00' AS potential_showtime
FROM movie
CROSS JOIN hall
LEFT JOIN showtime ON hall.hall_id = showtime.hall_id
   AND showtime.start_time < '2024-11-01 17:00:00'
   AND showtime.end_time > '2024-11-01 13:40:00'
WHERE movie.title = 'Опенгеймер' 
   AND showtime.showtime_id IS NULL;





