# Generated by Django 4.1.3 on 2022-12-04 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0030_transection_paying_commited_alter_orderstatus_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paying_amount',
        ),
    ]
