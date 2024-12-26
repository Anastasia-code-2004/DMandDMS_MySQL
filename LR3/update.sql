UPDATE movie
SET rating = 8.5
WHERE movie_id = 13;


UPDATE showtime
SET start_time = '2024-10-20 19:00:00', end_time = '2024-10-20 21:00:00'
WHERE showtime_id = 5;


UPDATE showtime
SET price = 19.00
WHERE hall_id = 4;


UPDATE review
SET description = 'Исправленный отзыв', rating = 9
WHERE review_id = 1;


UPDATE hall
SET name = 'Зал повышенного комфорта'
WHERE hall_id = 4;


UPDATE user_action_log
SET acttion_type = 'Написан отзыв'
WHERE user_action_log_id = 10;


UPDATE movie_genres
SET movie_id = 8
WHERE movie_id = 10 AND genre_id = 4;


UPDATE ticket
SET seat_id = 40
WHERE showtime_id = 4 AND seat_id = 37 AND user_id = 11;

ALTER TABLE movie
ALTER COLUMN title TYPE TEXT;

ALTER TABLE "user"
ADD COLUMN username VARCHAR(255);

ALTER TABLE user_action_log
RENAME COLUMN acttion_type TO action_type;

ALTER TABLE showtime
DROP COLUMN hall_id;
