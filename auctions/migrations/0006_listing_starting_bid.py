# Generated by Django 4.2.3 on 2023-08-10 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_current_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=10),
        ),
    ]