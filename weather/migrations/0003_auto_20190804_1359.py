# Generated by Django 2.2.4 on 2019-08-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_auto_20190804_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='city_id',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.CharField(max_length=100),
        ),
    ]
