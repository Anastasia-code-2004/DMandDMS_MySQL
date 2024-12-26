from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import LoginForm
from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Выполняем запрос для получения пользователя по имени
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, password, is_superuser
                    FROM "user"
                    WHERE email = %s
                """, [email])
                user = cursor.fetchone()

            if user and check_password(password, user[1]):  # Проверка пароля
                # Создание сессии
                request.session['user_id'] = user[0]
                request.session['is_superuser'] = user[2]

                messages.success(request, 'Вы успешно вошли в систему!')

                return redirect('home')  # Перенаправляем на каталог книг
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Проверка на совпадение паролей
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        # Проверка на уникальность пользователя
        with connection.cursor() as cursor:
            cursor.execute('SELECT user_id FROM "user" WHERE email = %s', [email])
            existing_user = cursor.fetchone()

            if existing_user:
                messages.error(request, 'Пользователь с таким логином или электронной почтой уже существует.')
                return redirect('register')

            hashed_password = make_password(password)
            cursor.execute('SET TIMEZONE = "Europe/Moscow";')
            # Создаем нового пользователя
            cursor.execute("""
                            INSERT INTO "user" (email, password, is_superuser, created_at)
                            VALUES (%s, %s, %s, NOW())
                        """, [email, hashed_password, False])

            user_id = cursor.lastrowid

        messages.success(request, 'Вы успешно зарегистрировались! Войдите в систему.')
        return redirect('login')

    return render(request, 'auth/register.html')