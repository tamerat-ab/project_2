# Generated by Django 4.2.4 on 2023-11-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_bids_bid_price_auction_list_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='is_active',
        ),
        migrations.AddField(
            model_name='bids',
            name='bid_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
