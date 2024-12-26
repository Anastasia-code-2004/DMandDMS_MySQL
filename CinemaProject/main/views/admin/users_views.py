from django.shortcuts import render
from django.db import connection

def admin_actions_list(request):
    # Получаем параметры сортировки из строки запроса
    sort_by = request.GET.get('sort_by', 'date')  # По умолчанию сортируем по дате
    order = request.GET.get('order', 'desc')     # По умолчанию сортировка по убыванию

    # Разрешенные поля для сортировки
    allowed_sort_fields = {'user_id', 'email', 'action_type', 'date'}
    if sort_by not in allowed_sort_fields:
        sort_by = 'date'  # Если поле не разрешено, сортируем по дате

    # Проверяем направление сортировки
    if order not in {'asc', 'desc'}:
        order = 'desc'  # Если направление не указано корректно, сортируем по убыванию

    # Формируем SQL-запрос с сортировкой
    query = f"""
        SELECT u.user_id, u.email, l.action_type, l.date AT TIME ZONE 'Europe/Minsk'
        FROM user_action_log l
        JOIN "user" u ON l.user_id = u.user_id
        ORDER BY {sort_by} {order.upper()}
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        # Преобразование в список словарей для удобства работы в шаблоне
        logs = [
            {
                'user_id': row[0],
                'email': row[1],
                'action_type': row[2],
                'date': row[3]
            }
            for row in rows
        ]

    # Передаем параметры сортировки в контекст для шаблона
    context = {
        'logs': logs,
        'sort_by': sort_by,
        'order': order
    }

    return render(request, 'admin/users_actions.html', context)
