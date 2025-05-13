import json

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView

from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.conf import settings

def auth_view(request):
    return render(request, 'registration/auth.html')

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        # Ваш код обработки AJAX-запроса
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Перенаправление после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def history(request):
    return render(request, 'history.html')

def squad(request):
    return render(request, 'squad.html')

def auth(request):
    return render(request, 'auth.html')

@csrf_exempt
def feedback_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Здесь обработка и сохранение feedback
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})



def auth_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('index')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Неверный логин или пароль'})

        return render(request, 'registration/auth.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'registration/auth.html')

TELEGRAM_BOT_TOKEN = '7381984415:AAErFdKYHx5vSIhS9-l4DGBjESrSHFsFuss'
TELEGRAM_CHAT_ID = '761940787'

import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # Правильный импорт settings


@csrf_exempt
def feedback_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            # Валидация данных
            if not all([name, email, message]):
                return JsonResponse({'success': False, 'error': 'Все поля обязательны для заполнения'})

            telegram_message = (
                f"Новое сообщение с сайта FC Barcelona!\n\n"
                f"Имя: {name}\n"
                f"Email: {email}\n"
                f"Сообщение: {message}"
            )

            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': telegram_message,
                'parse_mode': 'HTML'
            }

            response = requests.post(url, data=payload)
            response.raise_for_status()  # Генерирует исключение для статусов 4xx/5xx

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Неверный формат данных'})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': f'Ошибка Telegram API: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Внутренняя ошибка сервера: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'Метод не разрешен'}, status=405)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'registration/register.html'

def profile(request):
    return render(request, 'profile.html', {'user': request.user})