from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя"""
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ('username', 'first_name', 'last_name',)
        labels = {'username': 'Логин:',}
        help_texts = {'username': 'Должно быть уникально',}

class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя"""
    class Meta:
        model = CustomUser
        fields = '__all__'

class BookForm(forms.ModelForm):
    """Форма для работы с книгой"""
    class Meta:
        model = Books
        fields = '__all__'

class CommentForm(forms.ModelForm):
    """Форма для коментариев"""
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {'comment':forms.Textarea(attrs={'cols':80, 'rows':2})}