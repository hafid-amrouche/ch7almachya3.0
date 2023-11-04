# Generated by Django 4.1.2 on 2023-11-02 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_tokensessionid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokensessionid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='token_session_ids', to=settings.AUTH_USER_MODEL),
        ),
    ]