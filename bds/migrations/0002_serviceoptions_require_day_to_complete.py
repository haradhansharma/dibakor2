# Generated by Django 4.1.3 on 2022-11-29 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceoptions',
            name='require_day_to_complete',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
    ]
