from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

def admin_showtimes_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.showtime_id, s.start_time, s.price, 
                   m.title AS movie_title, h.name AS hall_name
            FROM showtime s
            JOIN movie m ON s.movie_id = m.movie_id
            JOIN hall h ON s.hall_id = h.hall_id
            ORDER BY s.showtime_id ASC
        """)
        rows = cursor.fetchall()

        # Преобразование в список словарей для удобства работы в шаблоне
        showtimes = [
            {
                'id': row[0],                # showtime_id
                'start_datetime': row[1],   # start_datetime
                'price': row[2],            # price
                'movie': row[3],            # movie_title
                'hall': row[4]              # hall_name
            }
            for row in rows
        ]

    return render(request, 'admin/showtimes.html', {'showtimes': showtimes})

from django.db import IntegrityError, OperationalError

def admin_edit_showtime(request, showtime_id=None):
    if showtime_id:
        # Получение показа для редактирования
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT showtime_id, start_time, price, movie_id, hall_id
                FROM showtime
                WHERE showtime_id = %s
            """, [showtime_id])
            row = cursor.fetchone()

        # Если показ не найден, возвращаем 404
        if not row:
            return get_object_or_404(showtime_id)

        showtime = {
            'id': row[0],
            'start_datetime': row[1],
            'price': row[2],
            'movie_id': row[3],
            'hall_id': row[4],
        }
    else:
        # Новый показ
        showtime = None

    # Получение списка фильмов и залов для выбора
    with connection.cursor() as cursor:
        cursor.execute("SELECT movie_id, title FROM movie ORDER BY title ASC")
        movies = cursor.fetchall()

        cursor.execute("SELECT hall_id, name FROM hall ORDER BY name ASC")
        halls = cursor.fetchall()

    if request.method == 'POST':
        start_datetime = request.POST.get('start_datetime')
        price = request.POST.get('price')
        movie_id = request.POST.get('movie_id')
        hall_id = request.POST.get('hall_id')

        try:
            with connection.cursor() as cursor:
                if showtime:
                    # Обновление существующего показа
                    cursor.execute("""
                        UPDATE showtime
                        SET start_time = %s, price = %s, movie_id = %s, hall_id = %s
                        WHERE showtime_id = %s
                    """, [start_datetime, price, movie_id, hall_id, showtime_id])
                else:
                    # Добавление нового показа
                    cursor.execute("""
                        INSERT INTO showtime (start_time, price, movie_id, hall_id)
                        VALUES (%s, %s, %s, %s)
                    """, [start_datetime, price, movie_id, hall_id])

            # После успешного выполнения запроса редиректим на список показов
            return redirect('admin_showtimes_list')

        except Exception as e:
            # Обработка всех других ошибок
            error_message = f"Произошла ошибка: {e}"
            return render(request, 'admin/showtime_form.html', {
                'showtime': showtime,
                'movies': movies,
                'halls': halls,
                'error_message': error_message
            })

    return render(request, 'admin/showtime_form.html', {
        'showtime': showtime,
        'movies': movies,
        'halls': halls,
    })


def admin_delete_showtime(request, showtime_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM showtime WHERE showtime_id = %s", [showtime_id])
    return redirect('admin_showtimes_list')
