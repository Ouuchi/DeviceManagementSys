# Generated by Django 4.1 on 2022-08-09 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wangapp', '0003_alter_device_apply_applypersonid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device_apply',
            name='state',
        ),
        migrations.AddField(
            model_name='device_apply',
            name='reason',
            field=models.TextField(default=None, verbose_name='理由'),
        ),
    ]
