# Generated by Django 3.2.8 on 2021-10-25 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_value', to='product.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('quantity', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVarient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varient_name', models.CharField(max_length=100)),
                ('old_price', models.FloatField()),
                ('price', models.FloatField(blank=True, null=True)),
                ('cost_price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('attribut_value', models.ManyToManyField(blank=True, related_name='attribute_product_varient', to='product.AttributeValue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_varient', to='product.product')),
            ],
        ),
    ]