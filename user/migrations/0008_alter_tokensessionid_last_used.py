# Generated by Django 4.1.2 on 2023-11-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_tokensessionid_last_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokensessionid',
            name='last_used',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
