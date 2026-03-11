# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов"""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Введите содержание поста'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, укажите заголовок',
                'max_length': 'Заголовок слишком длинный (макс. 200 символов)',
            },
            'content': {
                'required': 'Пожалуйста, напишите содержание поста',
            },
        }