# Generated by Django 5.1.5 on 2025-01-28 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_rename_author_monitoredstock_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoredstock',
            name='user',
        ),
    ]
