# Generated by Django 2.2 on 2019-04-23 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0005_auto_20190421_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartitem',
            name='date',
            field=models.IntegerField(),
        ),
    ]
