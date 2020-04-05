# Generated by Django 3.0.4 on 2020-03-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuildingBlocks', '0005_wishlistitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoldItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=500)),
                ('item_weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_price', models.BooleanField(default=False)),
            ],
        ),
    ]
