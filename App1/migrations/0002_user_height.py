# Generated by Django 2.2.4 on 2020-02-17 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.TextField(default=4),
            preserve_default=False,
        ),
    ]
