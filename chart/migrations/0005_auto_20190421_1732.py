# Generated by Django 2.2 on 2019-04-21 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0004_remove_chartticker_margins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartitem',
            name='date',
            field=models.DateField(),
        ),
    ]