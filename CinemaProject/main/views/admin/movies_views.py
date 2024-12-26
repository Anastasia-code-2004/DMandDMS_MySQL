import os
import uuid

from django.core.files.storage import default_storage
from django.db import connection
from django.shortcuts import render, redirect

def admin_movies_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT m.movie_id, m.title, m.release_date, m.duration, 
            m.poster, m.rating, m.description
            FROM movie m
            ORDER BY movie_id ASC""")
        movies = cursor.fetchall()

    return render(request, 'admin/movies.html', {'movies': movies})


def admin_edit_movie(request, movie_id=None):
    # Получаем информацию о фильме, если редактируем
    movie = None
    movie_genres = []
    if movie_id:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT movie_id, title, description, duration, 
                              poster, release_date, rating FROM movie WHERE movie_id = %s""",
                           [movie_id])
            row = cursor.fetchone()
            if row:
                movie = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'duration': row[3],
                    'poster': row[4],
                    'release_date': row[5],
                    'rating': row[6],
                }
            cursor.execute("SELECT genre_id FROM movie_genres WHERE movie_id = %s", [movie_id])
            movie_genres = [row[0] for row in cursor.fetchall()]

    # Получаем список всех жанров
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_id, name FROM genre")
        all_genres = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

    if request.method == 'POST':
        # Получаем данные из формы
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        duration = request.POST.get('duration', '')
        release_date = request.POST.get('release_date', None)  # Можно сделать преобразование даты, если нужно
        poster = request.FILES.get('poster', None)
        rating = request.POST.get('rating', None)  # Получаем рейтинг

        # Получаем список выбранных жанров
        genres = request.POST.getlist('genres')

        # Проверка, что хотя бы один жанр выбран
        if not genres:
            return render(request, 'admin/movie_form.html', {
                'movie': movie,
                'movie_genres': movie_genres,
                'all_genres': all_genres,
                'error_message': 'Пожалуйста, выберите хотя бы один жанр.'
            })

        # Если все обязательные данные получены корректно
        if not title or not duration:
            return render(request, 'admin/movie_form.html', {
                'movie': movie,
                'movie_genres': movie_genres,
                'all_genres': all_genres,
                'error_message': 'Название фильма и продолжительность обязательны для заполнения.'
            })

        # Обработка постера, если был загружен
        poster_path = None
        if poster:
            poster_path = save_poster(poster)

        # Обновляем или создаем фильм в базе данных
        with connection.cursor() as cursor:
            if movie_id:
                # Получаем текущий путь к постеру, если постер не передан
                if not poster:
                    cursor.execute("SELECT poster FROM movie WHERE movie_id = %s", [movie_id])
                    poster_path = cursor.fetchone()[0]

                # Обновляем существующий фильм
                cursor.execute("""
                    UPDATE movie
                    SET title = %s, description = %s, duration = %s, release_date = %s, rating = %s, poster = %s
                    WHERE movie_id = %s
                """, [title, description, duration, release_date, rating, poster_path, movie_id])

                # Обновляем связи с жанрами
                cursor.execute("DELETE FROM movie_genres WHERE movie_id = %s",
                               [movie_id])  # Если редактируем, удаляем старые жанры
                for genre_id in genres:
                    cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)",
                                   [movie_id, genre_id])
            else:
                cursor.execute("""INSERT INTO movie (title, description, duration, release_date, rating, poster)
                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING movie_id
                            """, [title, description, duration, release_date, rating, poster_path])
                movie_id = cursor.fetchone()[0]  # Получаем ID добавленного фильма

                # Добавляем связи с жанрами в таблицу `movie_genres`
                for genre_id in genres:
                    cursor.execute("""INSERT INTO movie_genres (movie_id, genre_id)
                                        VALUES (%s, %s) """, [movie_id, genre_id])

            # После успешного добавления или редактирования фильма, перенаправляем на страницу списка фильмов
            return redirect('admin_movies_list')

    return render(request, 'admin/movie_form.html', {
        'movie': movie,
        'movie_genres': movie_genres,
        'all_genres': all_genres,
    })


def admin_delete_movie(request, movie_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM movie WHERE movie_id = %s", [movie_id])
    return redirect('admin_movies_list')


def save_poster(poster):
    # Генерация уникального имени для файла
    unique_name = f"{uuid.uuid4().hex}{os.path.splitext(poster.name)[1]}"

    # Путь, куда будем сохранять файл
    poster_path = os.path.join('posters', unique_name)  # Папка 'posters' внутри 'media'

    # Сохранение файла в папку 'media/posters'
    file_path = default_storage.save(poster_path, poster)

    return unique_name