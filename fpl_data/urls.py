from django.urls import path
from .views import predictor_view, transaction_id_view, points_view

# app_name = 'fpl'

urlpatterns = [
    path('predict/<int:pk>', predictor_view, name='predict'),
    path('tid/', transaction_id_view, name='tid'),
    path('points/', points_view, name='points'),
]
