# Generated by Django 4.2.3 on 2023-07-25 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_no_of_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='no_of_products',
        ),
    ]
