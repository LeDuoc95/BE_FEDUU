# Generated by Django 3.1 on 2021-04-07 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20210405_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='new_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='old_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
