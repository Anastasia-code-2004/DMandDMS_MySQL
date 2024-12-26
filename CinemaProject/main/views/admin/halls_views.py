from django.db import connection
from django.shortcuts import render, redirect
from django.db import IntegrityError

def admin_halls_list(request):
    with connection.cursor() as cursor:
        # Получаем id и name для залов
        cursor.execute("SELECT hall_id AS id, name FROM hall ORDER BY hall_id ASC")
        halls = cursor.fetchall()

    # Преобразуем результат в список словарей для удобства работы в шаблоне
    halls = [{'id': hall[0], 'name': hall[1]} for hall in halls]

    return render(request, 'admin/halls.html', {'halls': halls})

def admin_add_hall(request):
    if request.method == 'POST':
        hall_name = request.POST.get('hall_name')
        rows_count = int(request.POST.get('rows_count'))
        seats_per_row = int(request.POST.get('seats_per_row'))

        try:
            with connection.cursor() as cursor:
                # Добавляем зал
                cursor.execute(
                    "INSERT INTO hall (name) VALUES (%s) RETURNING hall_id", [hall_name]
                )
                hall_id = cursor.fetchone()[0]

                # Генерируем места для зала
                for row in range(1, rows_count + 1):
                    for seat_number in range(1, seats_per_row + 1):
                        cursor.execute(
                            "INSERT INTO seat (hall_id, row, number) VALUES (%s, %s, %s)",
                            [hall_id, row, seat_number],
                        )

            return redirect('admin_halls_list')

        except IntegrityError:
            return render(request, 'admin/add_hall_form.html', {
                'error': 'Зал с таким именем уже существует. Пожалуйста, выберите другое имя.'
            })

    return render(request, 'admin/add_hall_form.html')



def admin_edit_hall(request, hall_id):
    if request.method == "POST":
        name = request.POST.get("name")
        # Обновляем информацию о зале
        with connection.cursor() as cursor:
            cursor.execute("UPDATE hall SET name = %s WHERE hall_id = %s", [name, hall_id])
        return redirect('admin_halls_list')

    # Получаем информацию о зале
    with connection.cursor() as cursor:
        cursor.execute("SELECT hall_id, name FROM hall WHERE hall_id = %s", [hall_id])
        hall = cursor.fetchone()

        # Получаем все места, связанные с залом
        cursor.execute("SELECT seat_id, row, number FROM seat WHERE hall_id = %s ORDER BY row, number ASC", [hall_id])
        seats = cursor.fetchall()

    # Преобразуем результаты в удобный формат
    hall = {'id': hall[0], 'name': hall[1]}
    seats = [{'id': seat[0], 'row': seat[1], 'number': seat[2]} for seat in seats]

    return render(request, 'admin/hall_form.html', {'hall': hall, 'seats': seats})


def admin_delete_hall(request, hall_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM hall WHERE hall_id = %s", [hall_id])
    return redirect('admin_halls_list')

def admin_add_seat(request, hall_id):
    if request.method == "POST":
        row = request.POST.get("row")
        number = request.POST.get("number")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO seat (hall_id, row, number) VALUES (%s, %s, %s)", [hall_id, row, number])
        return redirect('admin_edit_hall', hall_id=hall_id)

def admin_delete_seat(request, seat_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM seat WHERE seat_id = %s", [seat_id])
    return redirect(request.META.get('HTTP_REFERER', 'admin_halls_list'))
