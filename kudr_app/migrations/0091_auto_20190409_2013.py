# Generated by Django 2.1.4 on 2019-04-09 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0090_auto_20190409_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(blank=True, max_length=10000, verbose_name='Текст'),
        ),
    ]
