# Generated by Django 3.2.13 on 2022-06-28 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220627_0301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fpluser',
            name='referral_code',
        ),
        migrations.AddField(
            model_name='fpluser',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred', to='accounts.fpluser'),
        ),
        migrations.DeleteModel(
            name='Referral',
        ),
    ]
