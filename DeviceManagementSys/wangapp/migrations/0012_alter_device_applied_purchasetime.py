# Generated by Django 4.1 on 2022-08-10 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wangapp', '0011_device_laststate_device_applied_laststate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_applied',
            name='purchaseTime',
            field=models.DateField(default=None, verbose_name='设备购买时间'),
        ),
    ]
