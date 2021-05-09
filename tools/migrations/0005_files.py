# Generated by Django 3.1 on 2021-05-08 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_tools_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=20, null=True)),
                ('file', models.FileField(upload_to='uploads/')),
            ],
            options={
                'db_table': 'files_storage',
                'ordering': ['-id'],
            },
        ),
    ]
