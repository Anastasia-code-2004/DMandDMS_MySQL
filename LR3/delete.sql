DELETE FROM "user"
WHERE user_id = 14;


DELETE FROM user_action_log
WHERE user_id = 15;


DELETE FROM movie
WHERE movie_id = 8;


DELETE FROM movie_genres
WHERE movie_id = 10 AND genre_id = 6;


DELETE FROM review
WHERE movie_id = 2;


DELETE FROM genre
WHERE genre_id = 6;


DELETE FROM showtime
WHERE showtime_id = 5;


DELETE FROM seat
WHERE seat_id = 10;


DELETE FROM seat
WHERE hall_id = 5;


DELETE FROM movie
WHERE rating < 5;


ALTER TABLE movie
DROP COLUMN description;


DROP TABLE movie;


ALTER TABLE ticket
DROP CONSTRAINT ticket_showtime_id_fkey;


DROP INDEX idx_movie_title;
