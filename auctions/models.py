from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime



class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    pass
class Auction_list(models.Model):
    category_choices=(('CLOTHE','Clothe'),('SHOE','Shoe'),('BOOK','Book'),('BAGE','Bag'),('CAR','Car'),('NONE',None),)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    image =models.ImageField(upload_to='auction/images', blank=True , default=None)
    category = models.CharField (choices=category_choices,default=None, max_length=200, blank=True, null=True)
    is_active=models.BooleanField(default=True, null=True)

class Bids(models.Model):
    auction_item=models.ForeignKey(Auction_list, on_delete=models.CASCADE)  
    bid_price = models.IntegerField()
    # is_active=models.BooleanField(default=True, null=True)
    biding_user_id=models.IntegerField()
    
  
     

class Comments(models.Model):
    bids=models.ForeignKey(Auction_list, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)

    
class Watchlist(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    item_list=models.ForeignKey(Auction_list,on_delete=models.CASCADE)
    date_created=models.DateTimeField(default=datetime.now)
    item_id=models.IntegerField(null=False,blank=False)
   

