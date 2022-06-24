from django.contrib import admin
from .models import Prediction, fplUser, Token
# Register your models here.




admin.site.register(fplUser)
admin.site.register(Prediction)
admin.site.register(Token)