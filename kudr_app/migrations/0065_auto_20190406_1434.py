# Generated by Django 2.1.4 on 2019-04-06 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0064_auto_20190406_1356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concert',
            options={'ordering': ['begin_date'], 'verbose_name': 'Концерт', 'verbose_name_plural': 'Концерты'},
        ),
    ]
