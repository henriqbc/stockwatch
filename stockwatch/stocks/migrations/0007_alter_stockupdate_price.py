# Generated by Django 5.1.5 on 2025-02-02 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_alter_monitoredstock_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockupdate',
            name='price',
            field=models.FloatField(),
        ),
    ]
