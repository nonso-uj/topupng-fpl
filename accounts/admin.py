from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser, fplUser, Referral

# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'phone')

        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])

            if commit:
                user.save()
            return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'is_active', 'staff', 'admin')






class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active', 'staff')

    list_filter = ('is_active', 'staff', 'admin',)

    fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
    ('Permissions', {'fields': ('is_active', 'staff', 'admin',)}),
    )

    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
    }),
    )

    search_fields = ('email', 'first_name', 'last_name', 'phone',)
    ordering = ('email',)
    filter_horizontal = ()






admin.site.register(MyUser, UserAdmin)
admin.site.register(Referral)
admin.site.register(fplUser)
admin.site.unregister(Group)