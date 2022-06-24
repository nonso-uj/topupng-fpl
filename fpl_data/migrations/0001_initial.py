# Generated by Django 3.2.13 on 2022-06-22 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='fplUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.DecimalField(decimal_places=0, default=0, max_digits=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixture_id', models.CharField(max_length=255)),
                ('home_name', models.CharField(max_length=255)),
                ('away_name', models.CharField(max_length=255)),
                ('home_goals', models.CharField(max_length=2)),
                ('away_goals', models.CharField(max_length=2)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fpl_data.fpluser')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_id', models.CharField(max_length=5, unique=True, verbose_name='Transaction ID')),
                ('prediction', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fpl_data.prediction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fpl_data.fpluser')),
            ],
        ),
    ]
