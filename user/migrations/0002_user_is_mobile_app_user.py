# Generated by Django 3.2.8 on 2021-12-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_mobile_app_user',
            field=models.BooleanField(default=True),
        ),
    ]
