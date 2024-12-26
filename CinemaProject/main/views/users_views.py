from django.db import connection, IntegrityError
from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'home.html')


def profile_view(request):
    # Проверяем, авторизован ли пользователь
    user_id = request.session.get('user_id')

    if not user_id:
        # Если пользователь не авторизован, показываем ссылки на вход и регистрацию
        return render(request, 'profile.html', {
            'is_authenticated': False,
        })

    # Если пользователь авторизован, получаем его данные из базы
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT email, is_superuser
            FROM "user"
            WHERE user_id = %s
        """, [user_id])
        user = cursor.fetchone()

    if user:
        email, is_superuser = user
        return render(request, 'profile.html', {
            'is_authenticated': True,
            'email': email,
            'is_superuser': is_superuser,
        })
    else:
        request.session.flush()
        return redirect('login')


def my_tickets_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        # Если пользователь не авторизован, показываем ссылки на вход и регистрацию
        redirect('login')


    # Если пользователь авторизован, получаем его данные из базы
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT email, is_superuser
                FROM "user"
                WHERE user_id = %s
            """, [user_id])
        user = cursor.fetchone()

    if user[1]:
        return render(request, 'user_auth/my_tickets.html', {
            'error': 'У суперпользователей нет билетов!',
        })

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                t.purchase_date AT TIME ZONE 'Europe/Minsk' AS purchase_date,
                sh.price, 
                sh.start_time AS start_time, 
                h.name, 
                s.row, 
                s.number, 
                m.title, t.ticket_id
            FROM ticket t
            JOIN showtime sh ON sh.showtime_id = t.showtime_id
            JOIN seat s ON s.seat_id = t.seat_id
            JOIN "user" u ON u.user_id = t.user_id
            JOIN hall h ON h.hall_id = sh.hall_id
            JOIN movie m ON m.movie_id = sh.movie_id
            WHERE t.user_id = %s
        """, [user_id])
        tickets = cursor.fetchall()

    return render(request, 'user_auth/my_tickets.html', {
        'tickets': tickets
    })

def cancel_ticket(request, ticket_id):
    user_id = request.session.get('user_id')  # Получаем id текущего пользователя

    if not user_id:
        return redirect('login')  # Перенаправляем на страницу логина, если пользователь не авторизован

    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM ticket WHERE ticket_id = %s
        """, [ticket_id])

    return redirect('my_tickets')

def add_review_view(request, movie_id):
    user_id = request.session.get('user_id')

    if not user_id:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT email, is_superuser
                FROM "user"
                WHERE user_id = %s
            """, [user_id])
        user = cursor.fetchone()

    if user[1]:
        return render(request, 'user_auth/add_review.html', {
            'error': 'Суперпользователь не может оставить отзыв!',
        })

    # Получаем данные фильма
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT movie_id, title
            FROM movie
            WHERE movie_id = %s
        """, [movie_id])
        movie = cursor.fetchone()

    if not movie:
        return render(request, 'user_auth/add_review.html', {
            'error': 'Фильм не найден!',
        })

    # Если форма отправлена
    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Проверка: если текст отзыва пустой
        if not review_text:
            return render(request, 'user_auth/add_review.html', {
                'error': 'Отзыв не может быть пустым!',
                'movie_id': movie[0],
                'movie_title': movie[1]
            })

        # Проверка оценки на диапазон от 1 до 10
        try:
            rating = int(rating)
            if rating < 1 or rating > 10:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, 'user_auth/add_review.html', {
                'error': 'Оценка должна быть целым числом от 1 до 10!',
                'movie_id': movie[0],
                'movie_title': movie[1]
            })

        # Сохраняем отзыв в базе данных
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO review (movie_id, user_id, description, rating)
                    VALUES (%s, %s, %s, %s)
                """, [movie_id, user_id, review_text, rating])
        except Exception as e:
            return render(request, 'user_auth/add_review.html', {
                'error': {str(e)},
                'movie_id': movie[0],
                'movie_title': movie[1]
            })
        return redirect('movie_details', movie_id=movie_id)

    return render(request, 'user_auth/add_review.html', {
        'movie_id': movie[0],
        'movie_title': movie[1]
    })

def my_reviews_view(request):
    user_id = request.session.get('user_id')  # Получаем id текущего пользователя
    if not user_id:
        return redirect('login')

    # Получаем список отзывов текущего пользователя
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.description, r.rating, m.title, r.date AT TIME ZONE 'Europe/Minsk'
            FROM review r
            JOIN movie m ON m.movie_id = r.movie_id
            WHERE r.user_id = %s
            ORDER BY date DESC
        """, [user_id])
        reviews = cursor.fetchall()

    # Возвращаем список отзывов в шаблон
    return render(request, 'user_auth/my_reviews.html', {
        'reviews': reviews,
    })