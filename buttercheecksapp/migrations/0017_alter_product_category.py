# Generated by Django 4.2.2 on 2023-11-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttercheecksapp', '0016_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('BABY_SWADDLES', 'Baby Swaddles'), ('BABY_ROMBERS', 'Baby Rombers'), ('BABY_JABLAS', 'Baby Jablas'), ('BABY_BLANKETS', 'Baby Blankets'), ('BABY_BEDDINGS', 'Baby Beddings')], max_length=20, null=True),
        ),
    ]
