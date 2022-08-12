# Generated by Django 4.1 on 2022-08-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wangapp', '0010_device_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='lastState',
            field=models.SmallIntegerField(default=0, verbose_name='上一个状态'),
        ),
        migrations.AddField(
            model_name='device_applied',
            name='lastState',
            field=models.SmallIntegerField(default=0, verbose_name='上一个状态'),
        ),
        migrations.AddField(
            model_name='device_apply',
            name='lastState',
            field=models.SmallIntegerField(default=0, verbose_name='上一个状态'),
        ),
    ]
