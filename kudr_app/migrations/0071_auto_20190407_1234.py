# Generated by Django 2.1.4 on 2019-04-07 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0070_auto_20190407_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='danceinconcert',
            options={'ordering': ['concert'], 'verbose_name': 'Танец в концерте', 'verbose_name_plural': 'Танцы в концерте'},
        ),
        migrations.AlterModelOptions(
            name='participantdanceconcert',
            options={'ordering': ['participant_concert'], 'verbose_name': 'Участник-танец-концерт', 'verbose_name_plural': 'Участник-танец-концерт'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='participantdanceconcert',
            order_with_respect_to=None,
        ),
    ]
