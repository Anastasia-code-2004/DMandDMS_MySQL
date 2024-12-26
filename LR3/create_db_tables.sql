CREATE TABLE "user"(
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_superuser BOOL DEFAULT FALSE
);

CREATE TABLE movie(
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration INT CHECK (duration >= 0),
    poster BYTEA,
    release_date DATE,
    rating DECIMAL(3, 2) CHECK (rating BETWEEN 0 AND 10)
);

CREATE TABLE genre(
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE movie_genres(
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE hall(
    hall_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE seat(
    seat_id SERIAL PRIMARY KEY,
    hall_id INT NOT NULL,
    row SMALLINT NOT NULL,
    number SMALLINT NOT NULL,
    FOREIGN KEY (hall_id) REFERENCES hall(hall_id) ON DELETE CASCADE
);

CREATE TABLE showtime(
    showtime_id SERIAL PRIMARY KEY,
    movie_id INT NOT NULL,
    hall_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    price DECIMAL(6, 2) NOT NULL CHECK (price > 0),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (hall_id) REFERENCES hall(hall_id) ON DELETE CASCADE
);

CREATE TABLE ticket(
    ticket_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    seat_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES showtime(showtime_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seat(seat_id) ON DELETE CASCADE
);

CREATE TABLE review(
    review_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    description TEXT,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 10),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE
);

CREATE TABLE user_action_log(
    user_action_log_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acttion_type VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
)
PARTITION BY RANGE (EXTRACT(YEAR FROM date));

CREATE TABLE user_action_log_2023 PARTITION OF user_action_log
    FOR VALUES FROM (2023) TO (2024);

CREATE TABLE user_action_log_2024 PARTITION OF user_action_log
    FOR VALUES FROM (2024) TO (2025);
