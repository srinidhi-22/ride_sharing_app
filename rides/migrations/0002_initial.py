# Generated by Django 5.0.6 on 2024-06-14 07:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rides', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='companion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ride',
            name='companion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companion_rides', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ride',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traveler_rides', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='ride',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rides.ride'),
        ),
    ]