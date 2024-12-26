SELECT
    m.movie_id, 
    m.title, 
    AVG(r.rating) AS average_rating
FROM 
    movie AS m
INNER JOIN 
    review AS r ON m.movie_id = r.movie_id
GROUP BY 
    m.movie_id, 
    m.title
ORDER BY 
    average_rating DESC; -- Рейтинг фильма на основе отзывов

SELECT 
	user_id, 
   (SELECT email FROM "user" WHERE user_id = ticket.user_id),
    COUNT(ticket_id) AS ticket_count
FROM ticket
GROUP BY user_id;


SELECT
    s.showtime_id,
    s.movie_id,
	m.title,
    SUM(s.price) AS total_sales
FROM
    showtime AS s
JOIN
    ticket AS t ON s.showtime_id = t.showtime_id
JOIN
	movie AS m ON m.movie_id = s.movie_id
GROUP BY
    s.showtime_id, s.movie_id, m.title
ORDER BY
    s.showtime_id;

SELECT r.movie_id, m.title, AVG(r.rating) AS avg_rating
FROM review AS r
INNER JOIN movie AS m ON m.movie_id = r.movie_id
GROUP BY r.movie_id, m.title
HAVING AVG(r.rating) >= 7;

SELECT t.user_id, SUM(s.price) AS total_buy,
count(*)  as all
FROM ticket AS t
INNER JOIN showtime AS s ON s.showtime_id = t.showtime_id
GROUP BY user_id
HAVING SUM(s.price) > 20
ORDER BY total_buy DESC;

