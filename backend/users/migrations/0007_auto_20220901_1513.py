# Generated by Django 2.2.19 on 2022-09-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220901_1403'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique subscribe',
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='unique_subscribe'),
        ),
    ]
