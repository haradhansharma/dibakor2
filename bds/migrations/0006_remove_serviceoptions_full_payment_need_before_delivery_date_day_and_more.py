# Generated by Django 4.1.3 on 2022-11-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0005_serviceoptions_full_payment_need_before_delivery_date_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceoptions',
            name='full_payment_need_before_delivery_date_day',
        ),
        migrations.AddField(
            model_name='serviceoptions',
            name='full_payment_before_day',
            field=models.IntegerField(default=2, help_text='If partial payment then full payment should be paid before mentioned days of delivery date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serviceoptions',
            name='require_day_to_complete',
            field=models.IntegerField(help_text='Order need minimum days'),
        ),
    ]
