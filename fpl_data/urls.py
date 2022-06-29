from django.urls import path
from .views import predictor_view, transaction_id_view, points_view, scores_update, admin_dash, get_scores


urlpatterns = [
    path('predict/<int:pk>', predictor_view, name='predict'),
    path('tid/', transaction_id_view, name='tid'),
    path('points/', points_view, name='points'),
    path('scores/', scores_update, name='scores'),
    path('admin-dash/', admin_dash, name='admin-dash'),
    path('getScores/', get_scores, name='get-scores'),
]
