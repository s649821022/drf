# Generated by Django 2.1 on 2020-08-07 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookModel',
            new_name='Book',
        ),
    ]
