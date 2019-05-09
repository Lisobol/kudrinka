# Generated by Django 2.1.4 on 2019-04-01 11:39

from django.db import migrations, models
from Kudrinka.utils import unique_slug_generator


def update_slug(apps, schema_editor):
    obj = apps.get_model("kudr_app", "GroupChoreographerSchedule")

    for instance in obj.objects.all():
        if not instance.slug:
            instance.slug = unique_slug_generator(instance, instance.id, instance.slug)
            instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kudr_app', '0041_auto_20190401_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchoreographerschedule',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='URL'),
        ),
        migrations.RunPython(update_slug, reverse_code=migrations.RunPython.noop),

    ]
