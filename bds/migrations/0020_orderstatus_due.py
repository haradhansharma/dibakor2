# Generated by Django 4.1.3 on 2022-12-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0019_orderstatus_update_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='due',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
