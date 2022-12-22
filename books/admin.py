from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['first_name', 'last_name', 'books_name', 'comments',]
    list_display_links = ['first_name', 'last_name',]

    def books_name(self, obj):
        name = ''
        for book in obj.books_set.all():
            name += f'/{book}/'
        return name

    def comments(self, obj):
        return obj.comment_set.count()

class BooksAdmin(admin.ModelAdmin):
    model = Books
    list_display = ['name', 'get_user_name', 'comments']

    def get_user_name(self, obj):
        name = ''
        for user in obj.owner.all():
            name += f'/{user}/'
        return name
    
    def comments(self, obj):
        return obj.comment_set.count()

class CommentAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['comment', 'owner', 'book',]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Comment, CommentAdmin)
