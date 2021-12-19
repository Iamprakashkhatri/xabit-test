# Generated by Django 3.2.8 on 2021-12-16 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=511, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.URLField(blank=True)),
                ('description', models.TextField(default='-', max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='store.company')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=511, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.URLField(blank=True)),
                ('description', models.TextField(default='-', max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='product.productcategory')),
            ],
            options={
                'verbose_name': 'Product SubCategory',
                'verbose_name_plural': 'Product Sub-Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Object modified date and time')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Object created date and time')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=511, unique=True)),
                ('sku', models.CharField(blank=True, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('active', models.BooleanField(blank=True, default=True)),
                ('image', models.URLField(blank=True)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.productsubcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Object modified date and time')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Object created date and time')),
                ('price', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConsolidatedStoreProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consolidated_store_products', to='product.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consolidated_store_product', to='store.store')),
            ],
            options={
                'unique_together': {('store', 'product')},
            },
        ),
    ]
