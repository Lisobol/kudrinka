# Generated by Django 2.1.4 on 2019-05-11 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0100_auto_20190511_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 13, 9, 6, 665272), verbose_name='Дата'),
        ),
    ]
