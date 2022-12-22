from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

# app_name = 'books'

urlpatterns = [
    # Домашняя
    path('', views.home, name='home'),
    # Одна книга
    path('book/<int:pk>', views.book, name='book'),
    # Редактирование книги
    path('book-edit/<int:pk>', views.book_edit, name='book_edit'),
    # Удаление книгу
    path('book-delete/<int:pk>', views.book_delete, name='book_delete'),
    # Добавить книгу
    path('book-add/', views.book_add, name='book_add'),
    # Книга по авторам
    path('books-by-avtor/<int:user_id>', views.books_by_avtor, name='books_by_avtor'),

    # Изменить комментарий
    path('book/<int:book_id>/comment-edit/<int:comment_id>', views.comment_edit, name='comment_edit'),
    # Удалить комментарий
    path('book/<int:book_id>/comment-delete/<int:comment_id>', views.comment_delete, name='comment_delete'),

    # Регистрация и авторизация
    path('users/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]