# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post
from .forms import PostForm

# Статические страницы
def home(request):
    """Главная страница"""
    return render(request, 'blog/home.html')

def about(request):
    """Страница 'О нас'"""
    return render(request, 'blog/about.html')

# Классовые представления для постов
class PostListView(ListView):
    """Список всех постов"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5  # Пагинация по 5 постов на странице

class PostDetailView(DetailView):
    """Детальная страница поста"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    """Создание нового поста"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        """Действия при успешной валидации формы"""
        messages.success(self.request, 'Пост успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Действия при ошибках в форме"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)

class PostUpdateView(UpdateView):
    """Редактирование поста"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Пост успешно обновлён!')
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)

class PostDeleteView(DeleteView):
    """Удаление поста"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        """Логика удаления теперь здесь, а не в delete()"""
        messages.success(self.request, 'Пост успешно удалён!')
        return super().form_valid(form)