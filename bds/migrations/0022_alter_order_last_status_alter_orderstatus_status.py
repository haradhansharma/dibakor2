# Generated by Django 4.1.3 on 2022-12-04 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0021_invoicerecord_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='last_status',
            field=models.CharField(blank=True, default=None, max_length=152, null=True),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status',
            field=models.CharField(blank=True, choices=[('partialpaid', 'Partial Paid'), ('processing', 'Processing'), ('fullpaid', 'Full Paid'), ('pending', 'Pending'), ('progressing', 'Progressing'), ('hold', 'Hold'), ('complete', 'Complete'), ('unknown', 'Unknown')], default=None, max_length=20, null=True),
        ),
    ]
