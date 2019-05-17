# Generated by Django 2.1.4 on 2019-05-14 11:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0109_auto_20190514_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 14, 11, 28, 0, 172444, tzinfo=utc), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date_until',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 14, 11, 28, 0, 172444, tzinfo=utc), null=True, verbose_name='Дата, до которой объявление актуально'),
        ),
        migrations.AlterField(
            model_name='dance',
            name='name',
            field=models.TextField(max_length=80, verbose_name='Название танца'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 14, 11, 28, 0, 156487, tzinfo=utc), verbose_name='Дата'),
        ),
    ]
