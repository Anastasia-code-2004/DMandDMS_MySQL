CREATE OR REPLACE FUNCTION before_ticket_insert_fn()
RETURNS TRIGGER AS
$$
BEGIN
  -- Проверка, существует ли уже билет на это место и этот сеанс
  IF EXISTS (SELECT 1 FROM ticket WHERE showtime_id = NEW.showtime_id AND seat_id = NEW.seat_id) THEN
    RAISE EXCEPTION 'Билет на это место уже куплен на этот показ!';
  END IF;

  -- Возвращаем NEW, чтобы вставка прошла
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_ticket_insert
BEFORE INSERT ON ticket
FOR EACH ROW
EXECUTE FUNCTION before_ticket_insert_fn();

-- Здесь проверяется работа триггера
insert into ticket(user_id, showtime_id, seat_id)
values(11, 4, 36);


CREATE OR REPLACE FUNCTION before_showtime_insert_update_fn()	
RETURNS TRIGGER AS
$$
BEGIN
    -- Проверка, чтобы время начала не было в прошлом
    IF NEW.start_time <= NOW() THEN
        RAISE EXCEPTION 'Время показа некорректно!';
    END IF;

    -- Автоматическая установка end_time на основе длительности фильма
    NEW.end_time := NEW.start_time + 
                    (SELECT duration FROM movie WHERE movie_id = NEW.movie_id) * INTERVAL '1 minute';

    -- Проверка на пересечение сеансов в этом зале
    IF EXISTS (SELECT 1 FROM showtime
        WHERE hall_id = NEW.hall_id 
        AND 
        (
            -- Полное покрытие
            (NEW.start_time <= start_time AND NEW.end_time >= end_time) 
            -- Пересечение с концом
            OR (NEW.start_time < end_time AND NEW.start_time >= start_time) 
            -- Пересечение с началом
            OR (NEW.end_time > start_time AND NEW.end_time <= end_time) 
        )
    ) THEN 
        RAISE EXCEPTION 'Сеанс пересекается с другим сеансом в этом зале!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER before_showtime_insert_update
BEFORE INSERT OR UPDATE ON showtime
FOR EACH ROW
EXECUTE FUNCTION before_showtime_insert_update_fn();

select * from showtime;
insert into showtime(movie_id, hall_id, start_time, price)
values(6, 4, '2024-12-17 17:00:00', 10);


CREATE OR REPLACE FUNCTION log_user_action()
RETURNS TRIGGER AS
$$ 
BEGIN
	INSERT INTO user_action_log (user_id, action_type) 
    VALUES (NEW.user_id, TG_ARGV[0]); -- Аргумент TG_ARGV[0] 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Применение триггера на покупку билета
CREATE OR REPLACE TRIGGER ticket_purchase_log
AFTER INSERT ON ticket
FOR EACH ROW
EXECUTE FUNCTION log_user_action('Куплен билет');

-- Применение триггера на добавление отзыва
CREATE OR REPLACE TRIGGER review_log
AFTER INSERT ON review
FOR EACH ROW
EXECUTE FUNCTION log_user_action('Написан отзыв');

-- Применение триггера на регистрирование пользователя
CREATE OR REPLACE TRIGGER user_register_log
AFTER INSERT ON "user"
FOR EACH ROW
EXECUTE FUNCTION log_user_action('Зарегистрирован пользователь');


CREATE TRIGGER ticket_deletion_log 
AFTER DELETE ON ticket
FOR EACH ROW
EXECUTE FUNCTION log_user_action('Отказ от билета');


CREATE OR REPLACE FUNCTION prevent_duplicate_reviews()
RETURNS TRIGGER AS
$$
BEGIN
    -- Проверка на наличие существующего отзыва
    IF EXISTS (
        SELECT 1 FROM review 
        WHERE user_id = NEW.user_id AND movie_id = NEW.movie_id
    ) THEN
        RAISE EXCEPTION 'Вы уже оставляли отзыв на этот фильм!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER duplicate_review_check
BEFORE INSERT ON review
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_reviews();


CREATE OR REPLACE FUNCTION update_movie_rating()
RETURNS TRIGGER AS
$$
BEGIN
    -- Обновление среднего рейтинга фильма
    UPDATE movie
    SET rating = (
        SELECT ROUND(AVG(rating), 2)
        FROM review
        WHERE movie_id = NEW.movie_id
    )
    WHERE movie_id = NEW.movie_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER movie_rating_update
AFTER INSERT OR UPDATE ON review
FOR EACH ROW
WHEN (NEW.rating IS DISTINCT FROM OLD.rating)
EXECUTE FUNCTION update_movie_rating();


CREATE OR REPLACE FUNCTION prevent_superuser_deletion()
RETURNS TRIGGER AS
$$ 
BEGIN
	-- Проверка, если пользователь является суперпользователем
    IF OLD.is_superuser AND (SELECT COUNT(*) FROM "user" 
	WHERE is_superuser) = 1 THEN
        RAISE EXCEPTION 'Невозможно удалить суперпользователя!';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER superuser_deletion_prevention
BEFORE DELETE ON "user"
FOR EACH ROW
EXECUTE FUNCTION prevent_superuser_deletion();

drop trigger superuser_deletion_prevention ON "user";

