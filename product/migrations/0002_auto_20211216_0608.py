# Generated by Django 3.2.8 on 2021-12-16 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consolidatedstoreproduct',
            old_name='product',
            new_name='sku',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='product',
            new_name='sku',
        ),
        migrations.AlterUniqueTogether(
            name='consolidatedstoreproduct',
            unique_together={('store', 'sku')},
        ),
    ]
