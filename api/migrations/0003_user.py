# Generated by Django 2.1 on 2020-08-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200807_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('pwd', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=11)),
                ('sex', models.IntegerField(choices=[[0, '男'], [1, '女']], default=0)),
                ('icon', models.ImageField(default='icon/default.jpg', upload_to='icon')),
            ],
        ),
    ]
