# Generated by Django 5.0.4 on 2024-06-23 12:54
import random

from django.db import migrations


class Migration(migrations.Migration):

    def generate_barcodes(apps, schema_editor):
        Product = apps.get_model('main_app', 'Product')
        all_products = Product.objects.all()
        barcodes = random.sample(range(100000000, 1000000000), len(all_products))
        for product, barcode in zip(all_products, barcodes):
            product.barcode = barcode
            product.save()

    def reverse_barcodes(apps, schema_editor):
        Products = apps.get_model('main_app', 'Product')
        for products in Product.objects.all():
            products.barcode = 0
            products.save()

    dependencies = [
        ('main_app', '0004_product_barcode'),
    ]

    operations = [
        migrations.RunPython(generate_barcodes, reverse_barcodes),
    ]
