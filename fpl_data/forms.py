from django import forms
from .models import Prediction, Token

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['home_goals', 'away_goals']


class TokenForm(forms.ModelForm):
    class Meta:
        model= Token
        fields = ['t_id']