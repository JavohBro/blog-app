# Generated by Django 5.0.1 on 2024-03-26 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='edited_at',
        ),
    ]
