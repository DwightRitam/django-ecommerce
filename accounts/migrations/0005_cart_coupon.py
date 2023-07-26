# Generated by Django 4.2.3 on 2023-07-26 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_coupon'),
        ('accounts', '0004_alter_cartitem_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_coupon', to='products.coupon'),
        ),
    ]