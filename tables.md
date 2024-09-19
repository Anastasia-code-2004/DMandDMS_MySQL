# Таблицы:

### 1. users
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор пользователя._
  
- **password**: `VARCHAR(255) NOT NULL`  
  _Пароль пользователя, обязательное поле._
  
- **is_superuser**: `BOOL DEFAULT FALSE`  
  _Флаг, указывающий, является ли пользователь суперпользователем. По умолчанию FALSE._
  
- **email**: `VARCHAR(255) UNIQUE`  
  _Электронная почта пользователя, уникальное и обязательное поле._


### 2. clients
- **user_id**: `INT UNSIGNED PRIMARY KEY`  
  _Уникальный идентификатор пользователя, который служит внешним ключом и связывает запись в таблице `clients` с соответствующей записью в таблице `users`(связь один к одному). Это поле также является первичным ключом для таблицы `clients`._

- **first_name**: `VARCHAR(255)`  
  _Имя клиента._

- **last_name**: `VARCHAR(255)`  
  _Фамилия клиента._

- **phone_number**: `VARCHAR(20)`  
  _Телефонный номер клиента._
  
  
### 3. reviews
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор отзыва._
  
- **user_id**: `INT UNSIGNED NOT NULL`  
  _ID пользователя, который оставил отзыв, связь один ко многим._
  
- **movie_id**: `INT UNSIGNED NOT NULL`  
  _ID фильма, о котором написан отзыв, связь один ко многим._
  
- **description**: `VARCHAR(255)`  
  _Текст отзыва._
  
- **rating**: `TINYINT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 10)`  
  _Оценка фильма, значение от 1 до 10._
  
- **date**: `DATETIME DEFAULT CURRENT_TIMESTAMP`  
  _Дата создания отзыва (по умолчанию текущая дата и время)._


### 4. genres
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор жанра._
  
- **name**: `VARCHAR(100) NOT NULL UNIQUE`  
  _Название жанра, уникальное и обязательное поле._
  
- **description**: `VARCHAR(255)`  
  _Описание жанра._


### 5. movies
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор фильма._
  
- **title**: `VARCHAR(255) NOT NULL`  
  _Название фильма, обязательное поле._
  
- **description**: `TEXT`  
  _Описание фильма._
  
- **duration**: `INT UNSIGNED`  
  _Длительность фильма в минутах._
  
- **poster**: `BLOB`  
  _Постер фильма._
  
- **release_date**: `DATE`  
  _Дата релиза фильма._
  
- **rating**: `DECIMAL(3,2) CHECK (rating BETWEEN 0 AND 10)`  
  _Рейтинг фильма, значение от 0 до 10._


### 6. movie_genres
- **movie_id**: `INT UNSIGNED NOT NULL`  
- **genre_id**: `INT UNSIGNED NOT NULL`  
  _Связь многие ко многим таблиц movies и genres._


### 7. halls
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор зала._
  
- **name**: `VARCHAR(255) NOT NULL`  
  _Название зала, обязательное поле._


### 8. seats
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор места._
  
- **hall_id**: `INT UNSIGNED NOT NULL`  
  _ID зала, связь один ко многим._
  
- **row**: `TINYINT UNSIGNED NOT NULL`  
  _Номер ряда, обязательное поле._
  
- **number**: `TINYINT UNSIGNED NOT NULL`  
  _Номер места в ряду, обязательное поле._


### 9. showtimes
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор сеанса._
  
- **movie_id**: `INT UNSIGNED NOT NULL`  
  _ID фильма, который показывается на сеансе, связь один ко многим._
  
- **hall_id**: `INT UNSIGNED NOT NULL`  
  _ID зала, связь один ко многим._
  
- **start_time**: `DATETIME NOT NULL`  
  _Время начала сеанса, обязательное поле._
  
- **end_time**: `DATETIME NOT NULL`  
  _Время окончания сеанса, обязательное поле._
  
- **price**: `DECIMAL(6,2) NOT NULL CHECK (price > 0)`  
  _Цена билета, значение больше 0._



### 10. tickets
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор билета._
  
- **client_id**: `INT UNSIGNED NOT NULL`  
  _ID клиента, который купил билет, связь один ко многим._
  
- **showtime_id**: `INT UNSIGNED NOT NULL`  
  _ID сеанса, на который куплен билет, связь один ко многим._
  
- **seat_id**: `INT UNSIGNED NOT NULL`  
  _ID места, на которое куплен билет, связь один комногим._
  
- **purchase_date**: `DATETIME DEFAULT CURRENT_TIMESTAMP`  
  _Дата покупки билета (по умолчанию текущая дата и время)._
  

### 11. user_action_logs
- **id**: `INT UNSIGNED AUTO_INCREMENT PRIMARY KEY`  
  _Уникальный идентификатор записи в журнале действий._
  
- **user_id**: `INT UNSIGNED NOT NULL`  
  _ID пользователя, совершившего действие, связь один ко многим._
  
- **date**: `DEFAULT CURRENT_TIMESTAMP`  
  _Дата и время действия (по умолчанию текущая дата и время)._
  
- **action_type**: `VARCHAR(255) NOT NULL`  
  _Тип действия, например, "login", "logout", "buy_ticket"._

