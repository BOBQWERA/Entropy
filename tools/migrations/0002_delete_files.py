# Generated by Django 3.1 on 2021-05-04 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20210504_1907'),
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Files',
        ),
    ]
