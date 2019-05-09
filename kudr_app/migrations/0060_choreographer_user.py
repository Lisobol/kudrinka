# Generated by Django 2.1.4 on 2019-04-05 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kudr_app', '0059_costume_participantcostume'),
    ]

    operations = [
        migrations.AddField(
            model_name='choreographer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
