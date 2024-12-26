CREATE INDEX idx_movie_title ON movie (title);

CREATE INDEX idx_showtime_hall_id ON showtime (hall_id);
CREATE INDEX idx_showtime_movie_id ON showtime (movie_id);

CREATE INDEX idx_seat_hall_id ON seat (hall_id);

CREATE INDEX idx_review_movie_id ON review (movie_id);

CREATE INDEX idx_ticket_user_id ON ticket (user_id);
CREATE INDEX idx_ticket_showtime_id ON ticket (showtime_id);
CREATE INDEX idx_ticket_seat_id ON ticket (seat_id);

