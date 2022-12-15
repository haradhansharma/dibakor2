# Generated by Django 4.1.3 on 2022-12-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0025_alter_invoicerecord_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='transection',
            name='paying_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status',
            field=models.CharField(blank=True, choices=[('paid', 'Paid'), ('processing', 'Processing'), ('pending', 'Pending'), ('progressing', 'Progressing'), ('hold', 'Hold'), ('complete', 'Complete')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='transection',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]