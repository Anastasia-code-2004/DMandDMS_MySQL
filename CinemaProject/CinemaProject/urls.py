from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from main.views.admin.genres_views import admin_genres_list, admin_add_genre, admin_edit_genre, admin_delete_genre
from main.views.admin.halls_views import admin_halls_list, admin_edit_hall, admin_delete_hall, admin_add_seat, \
    admin_delete_seat, admin_add_hall
from main.views.admin.movies_views import admin_movies_list, admin_edit_movie, admin_delete_movie
from main.views.admin.showtimes_views import admin_showtimes_list, admin_edit_showtime, admin_delete_showtime
from main.views.admin.users_views import admin_actions_list
from main.views.auth_views import *
from main.views.booking_views import booking_ticket_details_view, booking_confirm_view
from main.views.movies_views import *
from main.views.showtimes_views import showtimes_view, showtime_details_view
from main.views.users_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'register/$', register_view, name='register'),
    re_path(r'login/$', login_view, name='login'),
    re_path(r'logout/$', logout_view, name='logout'),
    re_path(r'^$', home_view, name='home'),
    re_path(r'profile/$', profile_view, name='profile'),
    re_path(r'showtimes/$', showtimes_view, name='showtimes'),
    re_path(r'movies/$', movies_catalog_view, name='movies'),
    re_path(r'movie_details/(?P<movie_id>\d+)/$', movie_details_view, name='movie_details'),
    re_path(r'showtime_details/(?P<showtime_id>\d+)/$', showtime_details_view, name='showtime_details'),
    re_path(r'^showtime/(?P<showtime_id>\d+)/book/(?P<seat_id>\d+)/$', booking_ticket_details_view, name='book_ticket'),
    re_path(r'^booking/confirm/(?P<showtime_id>\d+)/(?P<seat_id>\d+)/$', booking_confirm_view, name='booking_confirm'),
    re_path(r'my_tickets/$', my_tickets_view, name='my_tickets'),
    re_path(r'^ticket/cancel/(?P<ticket_id>\d+)/$', cancel_ticket, name='cancel_ticket'),
    re_path(r'^movie/(?P<movie_id>\d+)/add_review/$', add_review_view, name='add_review'),
    re_path(r'my_reviews/$', my_reviews_view, name='my_reviews'),
    # CRUD для жанров
    path('genres/', admin_genres_list, name='admin_genres_list'),
    path('genres/add/', admin_add_genre, name='admin_add_genre'),
    path('genres/edit/<int:genre_id>/', admin_edit_genre, name='admin_edit_genre'),
    path('genres/delete/<int:genre_id>/', admin_delete_genre, name='admin_delete_genre'),
    # CRUD для фильмов
    path('admin_movies/', admin_movies_list, name='admin_movies_list'),
    path('movies/add/', admin_edit_movie, name='admin_add_movie'),
    path('movies/edit/<int:movie_id>/', admin_edit_movie, name='admin_edit_movie'),
    path('movies/delete/<int:movie_id>/', admin_delete_movie, name='admin_delete_movie'),
    # CRUD для показов
    path('admin_showtimes/', admin_showtimes_list, name='admin_showtimes_list'),
    path('showtimes/add/', admin_edit_showtime, name='admin_add_showtime'),
    path('showtimes/edit/<int:showtime_id>/', admin_edit_showtime, name='admin_edit_showtime'),
    path('showtimes/delete/<int:showtime_id>/', admin_delete_showtime, name='admin_delete_showtime'),
    # Действия пользователей
    path('admin_users_actions/', admin_actions_list, name='admin_actions_list'),
    # CRUD для залов
    path('admin_halls/', admin_halls_list, name='admin_halls_list'),  # Список залов
    path('halls/add/', admin_add_hall, name='admin_add_hall'),       # Добавление нового зала
    path('halls/edit/<int:hall_id>/', admin_edit_hall, name='admin_edit_hall'),  # Редактирование зала
    path('halls/delete/<int:hall_id>/', admin_delete_hall, name='admin_delete_hall'),  # Удаление зала
    path('seats/add/<int:hall_id>/', admin_add_seat, name='admin_add_seat'),
    path('seats/delete/<int:seat_id>/', admin_delete_seat, name='admin_delete_seat'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
