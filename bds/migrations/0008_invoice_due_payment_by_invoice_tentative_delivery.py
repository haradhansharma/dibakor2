# Generated by Django 4.1.3 on 2022-11-29 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0007_order_full_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_payment_by',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tentative_delivery',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
