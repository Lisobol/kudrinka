# Generated by Django 2.1.4 on 2019-04-04 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0056_auto_20190404_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantdanceconcert',
            name='num',
        ),
    ]
