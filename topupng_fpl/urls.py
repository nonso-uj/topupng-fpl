"""topupng_fpl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fpl_data.views import scores_view, reg_view, login_view, logoutUser, predictor_view, transaction_id_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', scores_view, name='home'),
    path('reg/', reg_view, name='reg'),
    path('login/', login_view, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('predict/<int:pk>', predictor_view, name='predict'),
    path('tid/', transaction_id_view, name='tid'),
]
