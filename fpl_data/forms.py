from django import forms
from .models import Prediction, Token

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['home_goals', 'away_goals']


class TokenForm(forms.ModelForm):
    t_id = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control w-75 mx-auto'
        }))
    class Meta:
        model= Token
        fields = ['t_id']