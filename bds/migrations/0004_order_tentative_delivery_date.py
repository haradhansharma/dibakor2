# Generated by Django 4.1.3 on 2022-11-29 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0003_alter_orderstatus_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tentative_delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
