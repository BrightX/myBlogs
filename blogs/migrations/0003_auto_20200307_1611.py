# Generated by Django 2.2.7 on 2020-03-07 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20200307_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='creat_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]
