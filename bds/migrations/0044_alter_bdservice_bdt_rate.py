# Generated by Django 4.1.3 on 2022-12-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0043_bdservice_bdt_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bdservice',
            name='bdt_rate',
            field=models.FloatField(default=101.8298, editable=False),
        ),
    ]
