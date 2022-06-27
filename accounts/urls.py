from django.urls import path
from .views import reg_view, login_view, logoutUser, activate

from django.contrib.auth import views as auth_views

# app_name = 'accounts'

urlpatterns = [
    path('reg/', reg_view, name='reg'),
    path('login/', login_view, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
