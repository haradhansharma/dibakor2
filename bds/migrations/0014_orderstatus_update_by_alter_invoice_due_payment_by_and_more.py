# Generated by Django 4.1.3 on 2022-11-30 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0013_alter_order_full_payment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='update_by',
            field=models.CharField(default='', max_length=252),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_payment_by',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='from_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='from_location',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='from_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='from_phone',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='orderinvoice', to='bds.order'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_amount',
            field=models.DecimalField(decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_require',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_require_file',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='order_status',
            field=models.CharField(max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method_isntruction',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method_title',
            field=models.CharField(max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_image',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_option_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_option_title',
            field=models.CharField(max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='service_title',
            field=models.CharField(max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='shipping_address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tentative_delivery',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='to_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='to_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='to_phone',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='invoicerecord',
            name='invoice_remarks',
            field=models.TextField(null=True),
        ),
    ]
