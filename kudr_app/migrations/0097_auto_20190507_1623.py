# Generated by Django 2.1.4 on 2019-05-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0096_auto_20190507_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choreographer',
            name='email',
            field=models.EmailField(blank=True, max_length=50, unique=True),
        ),
    ]
