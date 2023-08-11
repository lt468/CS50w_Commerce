# Generated by Django 4.2.3 on 2023-08-11 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite', to='auctions.listing'),
        ),
    ]
