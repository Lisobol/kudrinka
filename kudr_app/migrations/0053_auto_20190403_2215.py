# Generated by Django 2.1.4 on 2019-04-03 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0052_auto_20190403_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='name',
            field=models.TextField(blank=True, default='Концерт', max_length=50, verbose_name='Название концерта'),
        ),
    ]
