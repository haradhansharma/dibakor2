# Generated by Django 4.1.3 on 2022-12-04 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0026_transection_paying_amount_alter_orderstatus_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paying_amount',
            field=models.IntegerField(default=0),
        ),
    ]
