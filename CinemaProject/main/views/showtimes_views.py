from django.db import connection
from django.shortcuts import render

def showtimes_view(request):
    # Получаем параметры для сортировки и фильтрации из запроса
    search_title = request.GET.get('search_title', '')
    sort_by = request.GET.get('sort', 'start_time')  # По умолчанию сортировка по дате начала сеанса
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Получаем список жанров
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_id, name FROM genre")
        genres_list = cursor.fetchall()

    query = """
        SELECT DISTINCT s.showtime_id, m.movie_id, m.title, s.start_time, s.price, m.poster
        FROM showtime s
        JOIN movie m ON s.movie_id = m.movie_id
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genre g ON mg.genre_id = g.genre_id
    """
    conditions = []  # Условия для фильтрации

    # Фильтр по названию фильма
    if search_title:
        conditions.append(f"m.title ILIKE '{search_title}'")

    # Фильтр по жанрам
    if genres := request.GET.getlist('genre'):
        genre_ids = ','.join(genres)
        conditions.append(f"mg.genre_id IN ({genre_ids})")

    # Фильтр по дате начала сеанса
    if min_date:
        conditions.append(f"s.start_time >= '{min_date}'")
    if max_date:
        conditions.append(f"s.start_time <= '{max_date}'")

    # Фильтр по цене
    if min_price:
        conditions.append(f"s.price >= {min_price}")
    if max_price:
        conditions.append(f"s.price <= {max_price}")

    # Добавляем условия фильтрации в запрос
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Определяем порядок сортировки
    if sort_by == 'price':
        query += " ORDER BY s.price"
    elif sort_by == 'movie_title':
        query += " ORDER BY m.title"
    else:
        query += " ORDER BY s.start_time"

    # Выполняем SQL-запрос для получения сеансов
    with connection.cursor() as cursor:
        cursor.execute(query)
        showtimes = cursor.fetchall() # Для получения всех строк SQL-запроса

    # Формируем список словарей для передачи в шаблон
    showtimes_list = []
    for showtime in showtimes:
        showtimes_list.append({
            'id': showtime[0],
            'movie_id': showtime[1],
            'movie_title': showtime[2],
            'start_time': showtime[3],
            'price': showtime[4],
            'poster': showtime[5],
        })

    genres_data = [{'id': genre[0], 'name': genre[1]} for genre in genres_list]

    selected_genres = set(request.GET.getlist('genre'))

    context = {
        'showtimes': showtimes_list,
        'sort_by': sort_by,
        'genres': genres_data,
        'min_date': min_date,
        'max_date': max_date,
        'min_price': min_price,
        'max_price': max_price,
        'selected_genres': selected_genres,
    }

    return render(request, 'showtimes.html', context)


from django.db import connection
from django.shortcuts import render

def showtime_details_view(request, showtime_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                s.showtime_id, 
                s.start_time, 
                s.price, 
                m.movie_id, 
                m.title, 
                m.release_date, 
                m.duration, 
                m.poster, 
                m.rating, 
                m.description
            FROM showtime s
            JOIN movie m ON s.movie_id = m.movie_id
            WHERE s.showtime_id = %s
        """, [showtime_id])
        showtime = cursor.fetchone()

    # Проверка наличия данных
    if not showtime:
        return render(request, '404.html', status=404)

    # Формирование словаря с информацией о сеансе и фильме
    showtime_data = {
        'showtime_id': showtime[0],
        'start_time': showtime[1],
        'price': showtime[2],
        'movie': {
            'movie_id': showtime[3],
            'title': showtime[4],
            'release_date': showtime[5],
            'duration': showtime[6],
            'poster': showtime[7],
            'rating': showtime[8],
            'description': showtime[9],
        }
    }

    # Получение информации о местах
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM get_seats_for_showtime(%s);
        """, [showtime_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        seats = [dict(zip(columns, row)) for row in rows]

    # Передача данных в шаблон
    return render(request, 'showtime_details.html', {
        'showtime': showtime_data,
        'seats': seats,  # Список мест
    })
