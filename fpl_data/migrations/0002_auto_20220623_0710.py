# Generated by Django 3.2.13 on 2022-06-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpl_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fpluser',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='token',
            name='t_id',
            field=models.IntegerField(max_length=5, unique=True, verbose_name='Transaction ID'),
        ),
    ]