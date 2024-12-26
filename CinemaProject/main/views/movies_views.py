from datetime import datetime

from django.db import connection
from django.shortcuts import render


def movies_catalog_view(request):
    # Получаем параметры для сортировки и фильтрации из запроса
    search_title = request.GET.get('search_title', '')
    genres = request.GET.getlist('genre')  # Выбранные жанры
    sort_by = request.GET.get('sort', 'title')  # По умолчанию сортировка по названию
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    min_duration = request.GET.get('min_duration')
    max_duration = request.GET.get('max_duration')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')

    # Получаем список жанров
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_id, name FROM genre")
        genres_list = cursor.fetchall()

    query = """
        SELECT DISTINCT m.movie_id, m.title, m.release_date, m.duration, m.poster, m.rating
        FROM movie m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genre g ON mg.genre_id = g.genre_id
    """
    conditions = []  # Условия для фильтрации

    # Фильтр по названию
    if search_title:
        conditions.append(f"m.title ILIKE '{search_title}'")

    # Фильтр по жанрам
    if genres:
        genre_ids = ','.join(genres)
        conditions.append(f"mg.genre_id IN ({genre_ids})")

    # Фильтр по дате выхода
    if min_date:
        # Преобразуем min_date в формат 'YYYY-MM-DD'
        min_date_obj = datetime.strptime(min_date, '%Y-%m-%d').date()
        conditions.append(f"m.release_date >= '{min_date_obj}'")

    if max_date:
        # Преобразуем max_date в формат 'YYYY-MM-DD'
        max_date_obj = datetime.strptime(max_date, '%Y-%m-%d').date()
        conditions.append(f"m.release_date <= '{max_date_obj}'")

    # Фильтр по продолжительности
    if min_duration:
        conditions.append(f"m.duration >= {min_duration}")
    if max_duration:
        conditions.append(f"m.duration <= {max_duration}")

    # Фильтр по рейтингу
    if min_rating:
        conditions.append(f"m.rating >= {min_rating}")
    if max_rating:
        conditions.append(f"m.rating <= {max_rating}")

    # Добавляем условия фильтрации в запрос
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Определяем порядок сортировки
    if sort_by == 'release_date':
        query += " ORDER BY m.release_date"
    elif sort_by == 'duration':
        query += " ORDER BY m.duration"
    elif sort_by == 'rating':
        query += " ORDER BY m.rating"
    else:  # Default sorting by title
        query += " ORDER BY m.title"


    # Выполняем SQL-запрос для получения фильмов
    with connection.cursor() as cursor:
        cursor.execute(query)
        movies = cursor.fetchall()

    # Формируем список словарей для передачи в шаблон
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie[0],
            'title': movie[1],
            'release_date': movie[2],
            'duration': movie[3],
            'poster': movie[4],
            'rating': movie[5],
        })

    genres_data = [{'id': genre[0], 'name': genre[1]} for genre in genres_list]

    selected_genres = set(genres)

    context = {
        'movies': movies_list,
        'sort_by': sort_by,
        'genres': genres_data,
        'min_date': min_date,
        'max_date': max_date,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'min_rating': min_rating,
        'max_rating': max_rating,
        'selected_genres': selected_genres,
    }

    return render(request, 'movies.html', context)


def movie_details_view(request, movie_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.movie_id, m.title, m.release_date, m.duration, m.poster, m.rating, m.description
            FROM movie m
            WHERE m.movie_id = %s
        """, [movie_id])
        movie = cursor.fetchone()

    # Получаем жанры
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.name 
            FROM genre g
            JOIN movie_genres mg ON g.genre_id = mg.genre_id
            WHERE mg.movie_id = %s
        """, [movie_id])
        genres = cursor.fetchall()

    # Получаем отзывы
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.rating, r.description, r.date AT TIME ZONE 'Europe/Minsk', u.email 
            FROM review r
            JOIN "user" u ON r.user_id = u.user_id
            WHERE r.movie_id = %s
            ORDER BY r.date DESC
        """, [movie_id])
        reviews = cursor.fetchall()

    # Получаем сеансы на фильм
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.start_time, s.showtime_id
            FROM showtime s
            WHERE s.movie_id = %s
            ORDER BY s.start_time ASC
        """, [movie_id])
        showtimes = cursor.fetchall()


    movie_data = {
        'id': movie[0],
        'title': movie[1],
        'release_date': movie[2],
        'duration': movie[3],
        'poster': movie[4],
        'rating': movie[5],
        'description': movie[6],
        'genres': [genre[0] for genre in genres],
    }

    return render(request, 'movie_details.html', {
        'movie': movie_data,
        'reviews': reviews,
        'showtimes': showtimes,
    })