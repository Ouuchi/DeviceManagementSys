# Generated by Django 4.1 on 2022-08-09 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wangapp', '0002_device_apply_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_apply',
            name='applyPersonID',
            field=models.IntegerField(verbose_name='申请人ID'),
        ),
        migrations.AlterField(
            model_name='device_apply',
            name='deviceID',
            field=models.IntegerField(verbose_name='设备ID'),
        ),
    ]
