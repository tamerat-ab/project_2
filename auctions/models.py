from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    pass
class Auction_list(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    image =models.ImageField(upload_to='auction/images', max_length=20,height_field=20,width_field=20)
    # def __str__(self):
    #     return self.item_name
    
class Bids(models.Model):
    user =models.ForeignKey(Auction_list, on_delete=models.CASCADE)   
    category = models.CharField(max_length=200)
    bid_price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
     

class Comments(models.Model):
    bids=models.ForeignKey(Bids, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    
class Watchlist(models.Model):
    Auction_list=models.ForeignKey(Auction_list,on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    # def __unicode__(self):
    #     return self.
