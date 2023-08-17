from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from datetime import datetime



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
    if request.method == "POST":
        form =List_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_obj=form.instance
            return render(request, "auctions/create_listing.html", {'form':form, 'img_obj':img_obj})
    else:
         return render(request, "auctions/create_listing.html", {'create_listing':'create_listing'})
    # return HttpResponseRedirect(reverse("index"))   
        
        
def listing_page(request,id):
    item=Auction_list.objects.get(id=id)
    context={"auction":item}
    return render(request, "auctions/listing_page.html",context)
    

def delete_listing(request, id):
    item=Watchlist.objects.filter(auction_list=id)
    if item.exists():
     item.delete()
     message="the item deleted from the watchlist  successfully"
     return render(request,"Auctions/listing_page",{message:message})
    else:
         message="The item is not in the list"
         return render(request,"Auctions/listing_page",{message:message})
    # return HttpResponseRedirect(reverse("listing_page", args=(id)))
def watchlist(request):
    # Watchlist.objects.all()
    # Watchlist.id
    return render(request,'Auctions/watchlist.html')


#     item=Watchlist.objects.filter(auction_list=id)
#     # item_2=Watchlist.objects.filter(id=id)
#     if item.exists():
#         watched="watched"
#         return render(request,"Auctions/listing_page.html",{'watched':watched})
#     else:
#         return HttpResponseRedirect(reverse("watchlist", args=(id)))
#         return render(reverse("watchlist", args=(id)))

def update_bid(request ,id):
    if request.method=='POST':
        bid_price_new=request.POST.get('bid_price')
        bid_price_existed=Bids.objects.all()
        if bid_price_new > bid_price_existed:
            bid_price_existed.delete()
            bid_price_new.save()
            bid_price_new=Bids.objects.all()
            return render(request,'Auctions/listing_page.html',{"bid_price_new":bid_price_new})
        else:
            # please insert error handler here
            return render(request,'Auctions/listing_page.html',{'bid_price_error':'bid is not valied'})
def close_bid(request, id):
    user=request.user
    if user.is_authenticated():
        if user.Bids_set.all(id):
            bid_status=Bids.objects.filter(id=id)
            bid_status.is_active=False
    return render(request,'Auctions/listing_page.html',{"bid_status":"The bid is closed"})
def comment(request,id):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        return render(request,'Auctions/listing_page.html' ,{'comment':comment})
    
def add_to_watchlist(request, id):
    item_0=Auction_list.objects.get(id=id)
  
    item=Watchlist.objects.filter(item_list=item_0)
    if item:
        watched="watched"
        return render(request,"Auctions/listing_page.html",{'watched':watched})
    else:
        auction=Auction_list.objects.get(id=id)
        item_0.watchlist_set.create(date_created=datetime.now())
        # watchlist_item=Watchlist.objects.create(date_created=datetime.now(),item_list=Auction_list.objects.filter(id))
        # Watchlist.objects.create(date_created=datetime.now(),item_list=auction)
        # return HttpResponseRedirect(reverse('listing_page',args=(id,)))
        name=Watchlist.objects.get(id=id)
       
        # name=watchlist_item.item_name
        return render(request,'Auctions/watchlist.html',{'name':name, 'id':id})

def category(request):
    return render(request,'Auctions/category.html',{'category':'None'})
# def watched_item(request):



    
    


    



    







        




    


