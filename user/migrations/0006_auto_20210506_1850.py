# Generated by Django 3.1 on 2021-05-06 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210501_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_signed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
