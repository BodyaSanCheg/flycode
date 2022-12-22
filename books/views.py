from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import *
from .models import *

from django.contrib.auth.decorators import login_required # Проверка авторизованности пользователя


def home(request):
    """Отображение всех книг"""
    books = Books.objects.filter(archived = 0)
    context = {
        'books':books,
        }
    return render(request, 'home.html', context)

@login_required
def comment_edit(request, book_id, comment_id):
    """Изменение комментария"""
    comment = get_object_or_404(Comment, id=comment_id)

    check_comment_owner(request, comment)

    if request.method == 'POST':
        if CommentForm(instance=comment) != CommentForm(data=request.POST):
            form_comment_edit = CommentForm(instance=comment, data=request.POST)
            if form_comment_edit.is_valid:
                form_comment_edit.save()
                return redirect('book', pk=book_id)
    return redirect('book', pk=book_id)

def book(request, pk):
    """Отображение кокретной книги"""
    book = get_object_or_404(Books, pk=pk)
    
    if request.method == 'POST':
        # Добавление комментария
        form_comment_add = CommentForm(data=request.POST)
        if form_comment_add.is_valid:
            new_comment = form_comment_add.save(commit=False)
            new_comment.user = request.user
            new_comment.book = book
            new_comment.save()
            return redirect('book', pk=book.pk)
    else:
        form_comment_add = CommentForm()
        if request.GET.get('comment'):
            # Редактирование комментария
            try:
                comment_edit_id = int(request.GET.get('comment'))
            except:
                raise Http404
            comment = get_object_or_404(Comment, pk=comment_edit_id)


            check_comment_owner(request, comment)

            form_comment_edit = CommentForm(instance=comment)
        else:
            form_comment_edit = None
            comment_edit_id = None

    context = {
        'book':book,
        'form_comment_add':form_comment_add,
        'form_comment_edit':form_comment_edit,
        'comment_edit_id':comment_edit_id,
    }
    return render(request, 'books/book.html', context)

def books_by_avtor(request, user_id):
    """Отображение книг автора"""
    avtor = get_object_or_404(CustomUser, id=user_id)

    books = avtor.books_set.filter(archived = 0)
    context = {
        'books':books,
        'avtor':avtor
    }
    return render(request, 'books/books_by_avtor.html', context)

@login_required
def book_edit(request, pk):
    """Редактирование книги"""
    book = get_object_or_404(Books, pk=pk)

    
    check_book_owner(request, book)

    if request.method == 'POST':
        form = BookForm(instance=book, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('book', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    context = {
        'book':book,
        'form': form,
    }
    return render(request, 'books/book_edit.html', context)

@login_required
def book_delete(request, pk):
    """Удаление книги"""
    book = get_object_or_404(Books, pk=pk)

    check_book_owner(request, book)

    book.delete()
    return redirect('books_by_avtor', id=request.user.id)

@login_required
def comment_delete(request, book_id, comment_id):
    """Удаляет коментарий"""
    comment = get_object_or_404(Comment, id=comment_id)

    check_comment_owner(request, comment)

    comment.delete()
    return redirect('book', pk=book_id)

def check_book_owner(request, book):
    """Проверка, является ли пользователь владельцем"""
    if book.user != request.user:
        raise Http404

def check_comment_owner(request, comment):
    if comment.user != request.user:
        raise Http404

class SignUpView(CreateView):
    """Регистрация пользователя"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'