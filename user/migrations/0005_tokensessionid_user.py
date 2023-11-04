# Generated by Django 4.1.2 on 2023-11-02 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_tokensessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokensessionid',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
