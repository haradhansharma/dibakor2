# Generated by Django 4.1.3 on 2022-12-05 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0033_transection_vefiried_by_transection_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='transection',
            name='type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='transection',
            name='verified',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
