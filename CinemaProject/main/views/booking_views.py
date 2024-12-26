from django.shortcuts import render, redirect
from django.db import connection

def booking_ticket_details_view(request, showtime_id, seat_id):
    user_id = request.session.get('user_id')

    if not user_id:
        # Если пользователь не авторизован, показываем ссылки на вход и регистрацию
        return redirect('login')

    with (connection.cursor() as cursor):
        cursor.execute("""
            SELECT is_superuser, email
            FROM "user"
            WHERE user_id = %s
        """, [user_id])
        user = cursor.fetchone()

    if user[0]:
        return render(request, 'booking_ticket.html', {
            'error': 'Суперпользователи не могут бронировать билеты!',
        })

    with (connection.cursor() as cursor):
        cursor.execute("""
            SELECT s.row, s.number, h.name
            FROM seat s
            JOIN hall h ON h.hall_id = s.hall_id
            WHERE seat_id = %s
        """, [seat_id])
        seat = cursor.fetchone()

    with (connection.cursor() as cursor):
        cursor.execute("""
            SELECT s.start_time, s.price, m.title
            FROM showtime s
            JOIN movie m ON s.movie_id = m.movie_id
            WHERE showtime_id = %s
        """, [showtime_id])
        showtime = cursor.fetchone()

    ticket_data = {
        'user': {
            'user_id': user_id,
            'user_email': user[1],
        },
        'showtime': {
            'showtime_id': showtime_id,
            'movie': showtime[2],
            'price': showtime[1],
            'start_time': showtime[0],
        },
        'seat': {
            'seat_id': seat_id,
            'hall': seat[2],
            'row': seat[0],
            'number': seat[1],
        }
    }

    return render(request, 'booking_ticket.html', {'ticket' : ticket_data})

def booking_confirm_view(request, showtime_id, seat_id):
    user_id = request.session.get('user_id')

    if not user_id:
        # Если пользователь не авторизован, показываем ссылки на вход и регистрацию
        return redirect('login')

    # Проверка, является ли пользователь суперпользователем
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT is_superuser, email
            FROM "user"
            WHERE user_id = %s
        """, [user_id])
        user = cursor.fetchone()

    if user[0]:
        return render(request, 'booking_ticket.html', {
            'error': 'Суперпользователи не могут бронировать билеты!',
        })

    # Вызов процедуры для бронирования билета
    try:
        with connection.cursor() as cursor:
            # Вызов процедуры и получение выходного параметра
            cursor.execute("""
            CALL booking_ticket(%s, %s, %s);
            """, [user_id, showtime_id, seat_id])

        return redirect("showtimes")

    except Exception as e:
        return render(request, 'booking_ticket.html', {
            'error': f'Произошла ошибка: {str(e)}',
        })
