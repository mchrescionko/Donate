# Generated by Django 2.2.4 on 2020-02-17 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_user_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height2',
            field=models.TextField(default=33),
            preserve_default=False,
        ),
    ]