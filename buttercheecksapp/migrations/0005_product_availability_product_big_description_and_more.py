# Generated by Django 4.2.4 on 2023-09-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttercheecksapp', '0004_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='big_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('BABY_SWADDLES', 'Baby Swaddles'), ('BABY_ROMBERS', 'Baby Rombers'), ('BABY_JABLAS', 'Baby Jablas'), ('BABY_BLANKETS', 'Baby Blankets'), ('SHIRT_SHORTS', 'Shirt & Shorts')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
    ]