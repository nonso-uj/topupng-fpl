from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import fplUser
from django.contrib.auth import get_user_model

User = get_user_model()

# from django.contrib.auth.forms import UserCreationForm
# from myapp.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone',)
        exclude = ['username']
        




# class UserRegForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = '__all__'


