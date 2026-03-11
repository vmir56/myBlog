# blog/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Post

class PostModelTest(TestCase):
    """Тестирование модели Post"""
    
    def setUp(self):
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержание тестового поста'
        )
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.content, 'Содержание тестового поста')
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_str(self):
        self.assertEqual(str(self.post), 'Тестовый пост')
    
    def test_get_absolute_url(self):
        expected_url = reverse('blog:post_detail', args=[self.post.id])
        self.assertEqual(self.post.get_absolute_url(), expected_url)

class StaticPagesTest(TestCase):
    """Тестирование статических страниц"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_about_page(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

class PostViewsTest(TestCase):
    """Тестирование представлений для постов"""
    
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержание тестового поста'
        )
    
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Тестовый пост')
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Тестовый пост')
        self.assertContains(response, 'Содержание тестового поста')
    
    def test_post_create_view_get(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
    
    def test_post_create_view_post_valid(self):
        post_data = {
            'title': 'Новый пост',
            'content': 'Содержание нового поста'
        }
        response = self.client.post(reverse('blog:post_create'), post_data)
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertEqual(Post.objects.count(), 2)
        new_post = Post.objects.get(title='Новый пост')
        self.assertEqual(new_post.content, 'Содержание нового поста')
    
    def test_post_create_view_post_invalid(self):
        # Пустой заголовок
        post_data = {
            'title': '',
            'content': 'Содержание'
        }
        response = self.client.post(reverse('blog:post_create'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Пожалуйста, укажите заголовок')
        self.assertEqual(Post.objects.count(), 1)
    
    def test_post_update_view_get(self):
        response = self.client.get(reverse('blog:post_edit', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
        self.assertContains(response, self.post.title)
    
    def test_post_update_view_post(self):
        updated_data = {
            'title': 'Обновлённый заголовок',
            'content': 'Обновлённое содержание'
        }
        response = self.client.post(reverse('blog:post_edit', args=[self.post.id]), updated_data)
        self.assertRedirects(response, reverse('blog:post_detail', args=[self.post.id]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Обновлённый заголовок')
        self.assertEqual(self.post.content, 'Обновлённое содержание')
    
    def test_post_delete_view_get(self):
        response = self.client.get(reverse('blog:post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')
    
    def test_post_delete_view_post(self):
        response = self.client.post(reverse('blog:post_delete', args=[self.post.id]))
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertEqual(Post.objects.count(), 0)

class URLTests(TestCase):
    """Тестирование доступности URL"""
    
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(
            title='URL тест',
            content='Тест контент'
        )
    
    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_url(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_url(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_url(self):
        response = self.client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_url(self):
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_edit_url(self):
        response = self.client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_delete_url(self):
        response = self.client.get(f'/posts/{self.post.id}/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_post_url(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, 404)

class MessagesTest(TestCase):
    """Тестирование сообщений"""
    
    def setUp(self):
        self.client = Client()
    
    def test_create_success_message(self):
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'Тест',
            'content': 'Контент'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Пост успешно создан!' for msg in messages))
    
    def test_update_success_message(self):
        post = Post.objects.create(title='Старый', content='Контент')
        response = self.client.post(reverse('blog:post_edit', args=[post.id]), {
            'title': 'Новый',
            'content': 'Новый контент'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Пост успешно обновлён!' for msg in messages))
    
    def test_delete_success_message(self):
        post = Post.objects.create(title='Удаляемый', content='Контент')
        response = self.client.post(reverse('blog:post_delete', args=[post.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Пост успешно удалён!' for msg in messages))