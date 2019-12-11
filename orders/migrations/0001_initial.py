# Generated by Django 3.0 on 2019-12-06 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0002_cart_products'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(orders.models.OrderStatus['CREATED'], 'CREATED'), (orders.models.OrderStatus['PAYED'], 'PAYED'), (orders.models.OrderStatus['COMPLETED'], 'COMPLETED'), (orders.models.OrderStatus['CANCELED'], 'CANCELED')], default=orders.models.OrderStatus['CREATED'], max_length=50)),
                ('shopping_total', models.DecimalField(decimal_places=2, default=5, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
