# Generated by Django 4.2.4 on 2023-09-08 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttercheecksapp', '0002_size_remove_checkout_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancellation_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
