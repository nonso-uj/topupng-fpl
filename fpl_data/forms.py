from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Prediction, fplUser, Token


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['home_goals', 'away_goals']


class TokenForm(forms.ModelForm):
    class Meta:
        model= Token
        fields = ['t_id']