# Generated by Django 3.2.8 on 2021-10-21 17:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="useres",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
