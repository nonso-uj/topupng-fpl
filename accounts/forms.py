from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import fplUser
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()

# from django.contrib.auth.forms import UserCreationForm
# from myapp.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class':'form-control mb-3',
            'maxlength': "255",
            'placeholder':"Email*",
        }))
            # 'autofocus': "",
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control mb-3',
            'maxlength': "100",
            'placeholder':"First Name*",
        }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control mb-3',
            'maxlength': "100",
            'placeholder':"Last Name*",
        }))
    phone = PhoneNumberField(widget=forms.NumberInput(
        attrs={
            'class':'form-control mb-3',
            'placeholder':"Phone Number*",
        }))
    referrer = PhoneNumberField(widget=forms.NumberInput(
        attrs={
            'class':'form-control',
            'placeholder':"Referrers Phone Number*",
        }), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control mb-3',
            'autocomplete':"new-password",
            'placeholder':"Password*",
        }))
            # 'maxlength': "255",
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'form-control mb-3',
            'autocomplete':"new-password",
            'placeholder':"Confirm Password*",
        }))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone',)
        exclude = ['username']
        




# class UserRegForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = '__all__'


