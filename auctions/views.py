from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User , Auction_list ,Comments ,Bids ,Watchlist
from .forms import List_form


def index(request):
    
    active_listing=Auction_list.objects.all()
    if active_listing:
        
        return render(request, "auctions/index.html",{"active_listings":active_listing})
    else:
        return render(request, 'Actions/index.html',{'no_active_listings':'no_active_listings'})  


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

def create_listing(request):
    if request.method == "POST":
        form =List_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img_obj=form.instance
            return render(request, "auctions/creat_list.html", {'form':form, 'img_obj':img_obj})
    return HttpResponseRedirect(reverse("index"))   
        
        
def listing_page(request):
    item=Auction_list.objects.get(id=Auction_list.id)
    context={"item":item}
    return render(request, "auctions/listing_page.html",context)
    
    
    # def add_to_watchlist(id):
    #     watch_list=Watchlist.objects.filter(id=id)
    #     watch_list.save()
    #     return watch_list
def delete_listing(request, id):
    item=Watchlist.objects.filter(id=id)
    if item.exists():
     item.delete()
     message="the item deleted from the watchlist  successfully"
     return render(request,"Auctions/listing_page",{message:message})
    else:
         message="The item is not in the list"
         return render(request,"Auctions/listing_page",{message:message})
    # return HttpResponseRedirect(reverse("listing_page", args=(id)))
def add_to_list(request ,id):
    item_1=Auction_list.objects.filter(id=id)
    item_2=Watchlist.objects.filter(id=id)
    if item_2.exists():
        message="the item is already in the watchlist"
        return render(request,"Auctions/listing_page.html",{message:message})
def update_bid(request ,id):
    if request.method=='POST':
        bid_price_new=request.POST.get('bid_price')
        bid_price_existed=Bids.objects.all().bid_price
        if bid_price_new>bid_price_existed:
            bid_price_existed.delete()
            bid_price_new.save()
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

    
    


    



    







        




    


