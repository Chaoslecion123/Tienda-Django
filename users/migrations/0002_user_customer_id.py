# Generated by Django 3.0 on 2019-12-11 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='customer_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
