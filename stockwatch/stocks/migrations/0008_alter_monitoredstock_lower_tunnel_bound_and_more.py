# Generated by Django 5.1.5 on 2025-02-02 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_alter_stockupdate_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoredstock',
            name='lower_tunnel_bound',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='monitoredstock',
            name='upper_tunnel_bound',
            field=models.FloatField(),
        ),
    ]
