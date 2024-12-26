SELECT user_id, email
FROM "user" u
WHERE EXISTS (
    SELECT 1
    FROM review r
    JOIN ticket t ON t.user_id = r.user_id
    JOIN showtime s ON t.showtime_id = s.showtime_id
    WHERE r.user_id = u.user_id AND r.movie_id = s.movie_id
); -- Оставил ли пользователь отзыв на тот фильм, на который купил билет


SELECT movie_id, title
FROM movie m
WHERE EXISTS (
	SELECT 1
	FROM showtime s
	JOIN ticket t ON t.showtime_id = s.showtime_id
	WHERE s.movie_id = m.movie_id
); -- Фильмы, для которых есть сеансы и на эти сеансы курлены билеты


SELECT 
    h.name AS Зал,
    s.row AS Ряд,
    s.number AS Место,
    CASE 
        WHEN t.seat_id IS NULL THEN 'Свободно'
        ELSE 'Занято'
    END AS Статус
FROM 
    seat AS s
JOIN 
    hall AS h ON s.hall_id = h.hall_id
LEFT JOIN 
    ticket AS t ON s.seat_id = t.seat_id
LEFT JOIN 
	showtime ON showtime.showtime_id = t.showtime_id AND showtime.showtime_id = 6
WHERE 
    h.name = 'Зал 3';


SELECT 
    s.showtime_id,
	s.start_time,
    m.title AS movie,
    COUNT(t.ticket_id) OVER (PARTITION BY s.movie_id) AS total_tickets_sold,
    SUM(s.price) OVER (PARTITION BY s.movie_id) AS total_sales
FROM 
    ticket t
JOIN 
    showtime s ON t.showtime_id = s.showtime_id
JOIN 
    movie m ON s.movie_id = m.movie_id; -- Сеанс фильма, сколько продано билетов и общая сумма


SELECT r.user_id, u.email, r.rating,
AVG(r.rating) OVER (PARTITION BY r.user_id) AS avg_rating
FROM "user" AS u
JOIN review r ON u.user_id = r.user_id;

SELECT m.movie_id, m.title, m.rating, g.name,
DENSE_RANK() OVER (PARTITION BY g.name ORDER BY m.rating DESC) AS genre_rank
FROM movie m
JOIN movie_genres mg ON mg.movie_id = m.movie_id
JOIN genre g ON g.genre_id = mg.genre_id; -- Жанры, а в них фильмы ранжируются 
								-- в зависимости от значения рейтинга


