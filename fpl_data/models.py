from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class fplUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # counter = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Token(models.Model):
    t_id = models.IntegerField(verbose_name='Transaction ID', unique=True)
    user = models.ForeignKey(fplUser, on_delete=models.SET_NULL, null=True)
    # prediction = models.OneToOneField(Prediction, on_delete=models.SET_NULL, null=True, blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.t_id} for {self.user}"


class Prediction(models.Model):
    user = models.ForeignKey(fplUser, on_delete=models.CASCADE)
    fixture_id = models.CharField(max_length=255)
    home_name = models.CharField(max_length=255)
    away_name = models.CharField(max_length=255)
    home_goals = models.CharField(max_length=2)
    away_goals = models.CharField(max_length=2)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True, blank=True)
    # token = models.IntegerField(verbose_name='Transaction ID', unique=True)
    is_correct = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fixture_id} for {self.user}"




