# Generated by Django 4.1.3 on 2022-12-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0051_pickedorder_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bdservice',
            name='bdt_rate',
            field=models.FloatField(default=103.7228, editable=False),
        ),
    ]
