# Generated by Django 4.1.3 on 2022-12-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0028_remove_orderstatus_update_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='update_by',
            field=models.CharField(blank=True, editable=False, max_length=252, null=True),
        ),
    ]