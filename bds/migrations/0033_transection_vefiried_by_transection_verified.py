# Generated by Django 4.1.3 on 2022-12-05 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0032_alter_orderstatus_status_alter_transection_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='transection',
            name='vefiried_by',
            field=models.CharField(blank=True, editable=False, max_length=252, null=True),
        ),
        migrations.AddField(
            model_name='transection',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
