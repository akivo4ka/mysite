# Generated by Django 2.2.4 on 2019-08-06 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_city_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='city_id',
        ),
    ]