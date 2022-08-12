# Generated by Django 4.1 on 2022-08-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wangapp', '0005_device_apply_institution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_apply',
            name='state',
            field=models.SmallIntegerField(choices=[(0, '闲置'), (1, '已借出'), (2, '审批中')], default=0, verbose_name='设备状态'),
        ),
        migrations.AlterField(
            model_name='device',
            name='state',
            field=models.SmallIntegerField(choices=[(0, '闲置'), (1, '已借出'), (2, '审批中')], default=0, verbose_name='设备状态'),
        ),
    ]