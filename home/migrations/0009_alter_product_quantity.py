# Generated by Django 4.0.3 on 2024-07-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_product_product_id_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
