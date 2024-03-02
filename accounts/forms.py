from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterationForm(UserCreationForm):
    pass