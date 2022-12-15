# Generated by Django 4.1.3 on 2022-12-12 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0049_alter_bdservice_bdt_rate'),
        ('accounts', '0010_contractor_screening_done_userpayout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayout',
            name='payout_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payout_method', to='bds.paymentmethod'),
        ),
    ]