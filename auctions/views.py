from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.contrib import messages



from .models import User , Auction_list ,Comments ,Bids ,Watchlist
from .forms import List_form


def index(request):
    
    active_listing=Auction_list.objects.all()
    if active_listing:
        
        return render(request, "Auctions/index.html",{"active_listings":active_listing})
    else:
        return render(request, 'Auctions/index.html',{'no_active_listings':'no_active_listings'})  


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def list_form(request):
    context ={}
    context['form']= List_form()
    return render(request, "auctions/create_listing.html",context)

def create_listing(request):
    user=request.user
    form =List_form(request.POST,request.FILES or None)
    if request.method == "POST" and form.is_valid():
            item_name=form.cleaned_data.get('item_name')    
            price=form.cleaned_data.get('price')
            amount=form.cleaned_data.get('amount')
            image=form.cleaned_data.get('image')
            category=form.cleaned_data.get('category')
            auction=Auction_list(user=user,item_name=item_name,price=price,amount=amount,image=image,category=category)
            auction.save()
            # form.save()
            # img_obj=form.instance

            return render(request, "auctions/create_listing.html", {'form':form, 'img_obj':auction})
    else:
         return render(request, "auctions/create_listing.html", {'create_listing':'create_listing'})
    # return HttpResponseRedirect(reverse("index"))   
        
        
def listing_page(request,id):
    user=request.user
    item=Auction_list.objects.get(id=id)
    total_bid=Bids.objects.filter(auction_item=item).count()
    bid=Bids.objects.filter(auction_item=item).order_by('-id')[0]
    comment=Comments.objects.all()
    if request.method == "GET":
        if  Watchlist.objects.filter(item_id=id).exists():
            watch=Watchlist.objects.get(item_id=id)
            watch_count=Watchlist.objects.all().count()
            watched=watch.item_id
            bid=bid.bid_price
            bid_status=Bids.objects.filter(auction_item=item).order_by('-id')[0]
            status=bid_status.is_active
            biding_id=bid_status.biding_user_id
            context={"auction":item,'watch':  watched, 'bid':bid, 'total_bid':total_bid,
                    'status':status,'biding_id':biding_id,'comment':comment,'watch_count':watch_count}
            return render(request, "auctions/listing_page.html",context)
        else:
            return render(request, "auctions/listing_page.html",{"auction":item})
    


        
    

def delete_listing(request, id):
    item=Watchlist.objects.filter(item_id=id)
    if item.exists():
        item.delete()
        message="the item deleted from the watchlist  successfully"
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    else:
        message="The item is not in the list"
        return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    # return HttpResponseRedirect(reverse("listing_page", args=(id)))
def watchlist(request):
    user=request.user
    all_watchlist=Watchlist.objects.filter(user=user)
    print(all_watchlist)
    return render(request,'Auctions/watchlist.html',{'watchlist':all_watchlist})

def category(request):

    categories=['CLOTHE','SHOE','BOOK','BAGE','BAG','CAR','NONE']
    auction_item=Auction_list.objects.all()

    for category in categories:
         item=Auction_list.objects.filter(category=category)
 
    categories=['CLOTHE','SHOE','BOOK','BAGE','BAG','CAR','NONE']
    
    return render(request,'auctions/category.html',{'category':categories})   

def listing_category(request,category):
    auction_items=Auction_list.objects.filter(category=category)
    return render(request,'auctions/listing_category.html',{'category':auction_items}) 
         
                 
        


#     item_list=Auction_list.objects.all()
#     for item in item_list:
#         cat=item.category
#         category.append(cat)
#     category

#     for i in category:
#         # i=[i for i in item_list if i==item_list.category]
#         for item in item_list:
#             if i == item.category:
#                 i=[]
#             dict[i]=i.append(item.category)

   

def update_bid(request ,item_id):
    user=request.user
    if request.method =='POST':
       
        bid_price_new= int(request.POST.get('bid_price'))
        print(bid_price_new)
        auction_item=Auction_list.objects.get(id=item_id)
        biding_user = auction_item.user
        biding_user=User.objects.filter(auction_list=auction_item)[0].id
        print(biding_user)
        origional_price=auction_item.price
        if Bids.objects.filter(auction_item=auction_item).exists():
          bid_price_existed=Bids.objects.filter(auction_item=auction_item).order_by('-id')[0]
          if( bid_price_existed.is_active==True ) and  (bid_price_new > bid_price_existed.bid_price):  
            
                bid=Bids(auction_item=auction_item,bid_price=bid_price_new, is_active=True,biding_user_id=biding_user)
                bid.save()
                
                # bid_price_new=Bids.objects.filter(auction_item=auction_item)
                # return render(request,'auctions/listing_page.html',{"bid_price":bid_price_new, 'bid_id':id})
                return HttpResponseRedirect(reverse('listing_page', args=(item_id,)))
          else:
              messages.error(request,'invalid bid price')
              return HttpResponseRedirect(reverse('listing_page', args=(item_id,)))

        else:
            if int( bid_price_new) > int(origional_price):
                new_bid=Bids(auction_item=auction_item, bid_price=bid_price_new)
                new_bid.save()
             
                return HttpResponseRedirect(reverse('listing_page', args=(item_id,)))
            else:
                messages.error(request, 'invalid bid price')
                return HttpResponseRedirect(reverse('listing_page', args=(item_id,)))
         
        
def close_bid(request, id):
    user=request.user
    auction_item=Auction_list.objects.get(id=id)
    if Bids.objects.filter(auction_item=auction_item).exists:
        latest=Bids.objects.filter(auction_item=auction_item).order_by('-id')[0]
        latest.is_active=False
        latest.save()
    messages.success(request, 'the bid is closed successfully')
    return HttpResponseRedirect(reverse('listing_page', args=(id,)))
    return render(request,'Auctions/listing_page.html',{"bid_status":"The bid is closed"})

def comment(request,id):
    user=request.user
    if request.method=='POST':
        auction_item=Auction_list.objects.get(id=id)
        comment=request.POST.get('comment')
        comments=Comments(comment_text=comment, bids=auction_item)
        comments.save()
        return HttpResponseRedirect(reverse('listing_page', args=(id,)))
        # return render(request,'Auctions/listing_page.html' ,{'comment':comment})
    
def add_to_watchlist(request, id):
    user=request.user
    item=Auction_list.objects.get(id=id)
 
    watch=Watchlist.objects.filter(item_id=id)
    # if request.method == 'POST':
    if not watch.exists():
        watchlist=Watchlist(user=user,item_list=item,item_id=id)
        watchlist.save()
       
    return HttpResponseRedirect(reverse('listing_page',args=(id,)))
    
  
    





    
    


    



    







        




    


