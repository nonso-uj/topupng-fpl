# Generated by Django 3.2.13 on 2022-06-26 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='active',
            new_name='is_active',
        ),
    ]