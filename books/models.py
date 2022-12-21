from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Books(models.Model):
    """Описывает книги"""
    name = models.CharField(max_length=200, verbose_name='Книга',)
    description = models.TextField( blank=True, verbose_name='Содержимое',)
    archived = models.BooleanField(default=False, verbose_name='Архив',)
    owner = models.ManyToManyField('CustomUser', verbose_name='Авторы')
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Книги'
        verbose_name = 'Книга'
        ordering = ['-date_added'] # сортировка

    def __str__(self) -> str:
        return self.name

class Comment(models.Model):
    """Описывает комментарии авторов"""
    comment = models.TextField(max_length=500, verbose_name='Комментарий',)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE,)
    book = models.ForeignKey('Books', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Коментарии'
        ordering = ['-date_added'] # сортировка

    def __str__(self) -> str:
        return  f"{self.comment[:50]}..." if len(self.comment)>50 else f"{self.comment}"

class CustomUser(AbstractUser):
    """Описывает профиль Автора"""
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='profile/', verbose_name='Аватарка',)

    def __str__(self) -> str:
        return self.first_name

class Photo(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE,)
    avatar = models.ImageField(upload_to='media/photo/', verbose_name='Аватарка',)