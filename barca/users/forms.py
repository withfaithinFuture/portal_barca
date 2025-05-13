from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Только буквы, первая заглавная',
        validators=[RegexValidator(r'^[А-ЯЁ][а-яё]+$', 'Только буквы, первая заглавная')]
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text='Только буквы, первая заглавная',
        validators=[RegexValidator(r'^[А-ЯЁ][а-яё]+$', 'Только буквы, первая заглавная')]
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']