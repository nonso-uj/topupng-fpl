from django.urls import path
from .views import predictor_view, transaction_id_view, points_view, scores_update, admin_dash, get_scores, get_predicts, stop_calls, user_predictions


urlpatterns = [
    path('predict/<int:pk>', predictor_view, name='predict'),
    path('tid/', transaction_id_view, name='tid'),
    path('points/', points_view, name='points'),
    path('scores/', scores_update, name='scores'),
    path('admin-dash/', admin_dash, name='admin-dash'),
    path('getScores/', get_scores, name='get-scores'),
    path('getPredicts/', get_predicts, name='get-predicts'),
    path('stop-calls/', stop_calls, name='stop-calls'),
    path('predictions/<int:pk>', user_predictions, name='predictions'),
]
