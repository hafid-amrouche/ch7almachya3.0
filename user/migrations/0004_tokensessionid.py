# Generated by Django 4.1.2 on 2023-11-02 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_notificationstoken_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenSessionId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=256)),
                ('session_id', models.CharField(max_length=256)),
            ],
        ),
    ]
