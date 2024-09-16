# Таблицы:


1. users
  -**id**           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор пользователя._
  
  -**password**	VARCHAR(255) NOT NULL
  _Пароль пользователя, обязательное поле._
  
  -**is_superuser** BOOL DEFAULT FALSE
  _Флаг, указывающий, является ли пользователь суперпользователем._
  По умолчанию FALSE.
  
  -**username**     VARCHAR(255) UNIQUE
  _Имя пользователя, уникальное и обязательное поле._
  
  -**email**        VARCHAR255() UNIQUE
  _Электронная почта пользователя, уникальное и обязательное поле._
  
2. reviews
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _ Уникальный идентификатор отзыва._
  
  -**user_id**		INT UNSIGNED NOT NULL
  _ID пользователя, который оставил отзыв, один ко многим._
  
  -**movie_id**	INT UNSIGNED NOT NULL
  _ID фильма, о котором написан отзыв, один ко многим._
  
  -**description**  VARCHAR(255)
  _Текст отзыва._
  
  -**rating** 		TINYINT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 10)
  _Оценка фильма, значение от 1 до 10._
  
  -**date**		DATETIME DEFAULT CURRENT_TIMESTAMP
  _Дата создания отзыва (по умолчанию текущая дата и время)._
  
3. genres
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор жанра._
  
  -**name**		VARCHAR(100) NOT NULL UNIQUE
  _Название жанра, уникальное и обязательное поле._
  
  -**description**  VARCHAR(255)
  _Описание жанра._
  
4. persons
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор персоны._
  
  -**full_name**	VARCHAR(255) NOT NULL
  _Полное имя персоны, обязательное поле._
  
  -**photo**		BLOB	
  _Фото персоны._
  
  -**birth_date**	DATE
  _Дата рождения персоны._
  
5. movies
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор фильма._
  
  -**title**		VARCHAR(255) NOT NULL
  _Название фильма, обязательное поле._
  
  -**description**  TEXT  
  _Описание фильма._
    
  -**director_id**  INT UNSIGNED
  _ID режиссера фильма, связь один ко многим._
  
  -**duration**     INT UNSIGNED
  _Длительность фильма в минутах._
  
  -**poster**	    BLOB
  _Постер фильма._
  
  -**release_date** DATE    
  _Дата релиза фильма._
     
  -**rating**		DECIMAL(3,2) CHECK (rating BETWEEN 0 AND 10)
  _Рейтинг фильма, значение от 0 до 10._
  
6.movie_genres
  -**movie_id**	INT UNSIGNED NOT NULL
  -**genre_id**	INT UNSIGNED NOT NULL
  _Связь многие ко многим таблиц movies и genres._
  
7. halls
  -**id**		INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор зала._
  
  -**name**	VARCHAR(255) NOT NULL 
  _Название зала, обязательное поле._
  
8. hall_seats
  -**id**		INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор места._
  
  -**hall_id**  INT UNSIGNED NOT NULL
  _ID зала, связь один к одному._
  
  -**row**		TINYINT UNSIGNED NOT NULL
  _Номер ряда, обязательное поле._
  
  -**seats**	TINYINT UNSIGNED NOT NULL
  _Количество мест в ряду, обязательное поле._
  
9. showtimes
  -**id**		INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор сеанса._
  
  -**movie_id**	INT UNSIGNED NOT NULL
  _ID фильма, который показывается на сеансе, связь один ко многим._
  
  -**hall_id**		INT UNSIGNED NOT NULL
  _ID зала, связь один ко многим._
  
  -**start_time** 	DATETIME NOT NULL
  _Время начала сеанса, обязательное поле._
  
  -**end_time**	DATETIME NOT NULL
  _Время окончания сеанса, обязательное поле._
  
  -**price**	DECIMAL(6,2) NOT NULL CHECK (price > 0)
  _Цена билета, значение больше 0, максимальное кол-во цифр 6, кол-во цифр после запятой - 2._
  
10. booked_seats
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор забронированного места._
  
  -**showtime_id**   INT UNSIGNED NOT NULL
  _ID сеанса, связь один к одному._
  
  -**row**		TINYINT UNSIGNED NOT NULL
  _Номер ряда забронированного места._
  
  -**number**	TINYINT UNSIGNED NOT NULL
  _Номер забронированного места._
  
11. tickets
  -**id**		INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор билета._
  
  -**user_id**	INT UNSIGNED NOT NULL
  _ID пользователя, который купил билет, связь один ко многим._
  
  -**booked_seat_id** INT UNSIGNED NOT NULL
  _ID забронированного места, связь один к одному._
  
  -**purchase_date**  DATETIME DEFAULT CURRENT_TIMESTAMP
  _Дата покупки билета (по умолчанию текущая дата и время)._
  
12. user_action_logs
  -**id**			INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
  _Уникальный идентификатор записи в журнале действий._
  
  -**user_id**		INT UNSIGNED NOT NULL
  _ID пользователя, совершившего действие, связь один ко многим._
  
  -**date**      	DEFAULT CURRENT_TIMESTAMP
  _Дата и время действия (по умолчанию текущая дата и время)._
  
  -**action_type**   VARCHAR(255) NOT NULL 
  _Тип действия, например, "login", "logout", "buy_ticket"._
