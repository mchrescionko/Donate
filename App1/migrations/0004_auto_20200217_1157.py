# Generated by Django 2.2.4 on 2020-02-17 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0003_user_height2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='height',
        ),
        migrations.RemoveField(
            model_name='user',
            name='height2',
        ),
    ]
