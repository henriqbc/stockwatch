# Generated by Django 5.1.5 on 2025-01-29 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_remove_monitoredstock_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoredstock',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
