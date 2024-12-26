from django.db import connection, IntegrityError
from django.shortcuts import render, redirect

def admin_genres_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_id, name, description FROM genre ORDER BY genre_id ASC")
        genres = cursor.fetchall()

    return render(request, 'admin/genres.html', {'genres': genres})

def admin_add_genre(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')

        # Проверяем, существует ли уже жанр с таким именем
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM genre WHERE name = %s", [name])
            genre_exists = cursor.fetchone()[0] > 0

        if genre_exists:
            # Если жанр уже существует, отправляем сообщение об ошибке
            error_message = f"Жанр с именем '{name}' уже существует."
            return render(request, 'admin/genre_form.html', {'error_message': error_message})

        try:
            # Вставляем новый жанр в базу данных
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO genre (name, description) VALUES (%s, %s)", [name, description])
        except IntegrityError:
            # Обрабатываем исключение, если жанр с таким именем все-таки существует (можно повторно обработать)
            error_message = f"Ошибка при добавлении жанра: '{name}' уже существует."
            return render(request, 'admin/genre_form.html', {'error_message': error_message})

        return redirect('admin_genres_list')

    return render(request, 'admin/genre_form.html')


def admin_edit_genre(request, genre_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')

        # Проверяем, существует ли уже жанр с таким именем, кроме текущего
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM genre WHERE name = %s AND genre_id != %s", [name, genre_id])
            genre_exists = cursor.fetchone()[0] > 0

        if genre_exists:
            # Если жанр с таким именем уже существует, отправляем сообщение об ошибке
            error_message = f"Жанр с именем '{name}' уже существует."
            # Получаем данные жанра для отображения в форме
            with connection.cursor() as cursor:
                cursor.execute("SELECT genre_id, name, description FROM genre WHERE genre_id = %s", [genre_id])
                genre = cursor.fetchone()
            genre = {
                'id': genre[0],
                'name': genre[1],
                'description': genre[2]
            }
            return render(request, 'admin/genre_form.html', {'genre': genre, 'error_message': error_message})

        try:
            # Обновляем жанр в базе данных
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE genre
                    SET name = %s, description = %s
                    WHERE genre_id = %s
                """, [name, description, genre_id])
        except IntegrityError:
            # Обрабатываем исключение, если произошла ошибка обновления
            error_message = f"Ошибка при обновлении жанра: '{name}'."
            return render(request, 'admin/genre_form.html', {'error_message': error_message})

        return redirect('admin_genres_list')

    # Получаем жанр для редактирования
    with connection.cursor() as cursor:
        cursor.execute("SELECT genre_id, name, description FROM genre WHERE genre_id = %s", [genre_id])
        genre = cursor.fetchone()

    genre = {
        'id': genre[0],
        'name': genre[1],
        'description': genre[2]
    }
    return render(request, 'admin/genre_form.html', {'genre': genre})

def admin_delete_genre(request, genre_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM genre WHERE genre_id = %s", [genre_id])
    return redirect('admin_genres_list')