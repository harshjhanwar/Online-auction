from email import message
from email.policy import default
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import *
from .forms import *



def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all(),
        "tag" : "Active Listings"
    })

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

@login_required
def create(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        form.instance.creator = request.user

        if form.is_valid():
            img = request.POST.get("image", default=False)
            if not img:
                form.instance.image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSW60dxlZFu7li68JtK3wtJjY0gJccdzCioNF8y-hrxQ&s"
                print("not")
            obj = form.save()
            category = request.POST.get("c", default=False)
            if category:
                c, created = Category.objects.get_or_create(name = category)
                c.listings.add(obj)
            return redirect('listing', id=obj.id)
        
        return render(request, "auctions/create.html",{
            "form" : form,
        })
        # title = request.POST["title"]
        # description = request.POST["description"]
        # starting_bid = request.POST["bid"]
        # image = request.POST["image"]
        # Listing.objects.create(title=title, description=description, starting_bid=starting_bid, image=image, creator=request.user)
        # return redirect('index')
    
    form = NewListing()
    return render(request, "auctions/create.html",{
        "form" : form,
    })

def listing(request, id):
    obj = Listing.objects.get(pk = id)
    a = False
    if request.user.is_authenticated:
        if Watchlist.objects.filter(user = request.user, listing=obj).exists():
            a = True
    
    winner = ""
    if not obj.is_active:
        winner = Bids.objects.filter(bid = obj.current_bid).first()
    if request.method == "POST":
        if 'place_bid' in request.POST:
            price = request.POST['bid']
            if price:
                if float(price)>obj.current_bid:
                    obj.current_bid = price
                    obj.save(update_fields = ['current_bid'])
                    Bid, created = Bids.objects.update_or_create(
                        bidder = request.user, listing=obj,
                        defaults = {'bid' : price})
                    return redirect('listing', id=id)
            messages.error(request, f"Bid must be greater than {obj.current_bid}")
            return redirect('listing',id=id)
        else:
            comment = request.POST['comment']
            comments.objects.create(comment=comment, writer = request.user, listing=obj)
            return redirect('listing', id=id)
    
    c = obj.comments.all()
    return render(request, "auctions/listing.html", {
        "obj" : obj,
        'comment' : c,
        "a" : a,
        "winner" : winner
    })

@login_required
def watchlist(request):
    obj = Watchlist.objects.filter(user = request.user).first()
    if obj:
        l = obj.listing.all()
    else:
        l = []
    return render(request, "auctions/index.html", {
        "listings" : l,
        "tag" : "Watchlist"
    })

def close(request, id):
    obj = get_object_or_404(Listing, pk=id)
    obj.is_active = False
    obj.save(update_fields = ['is_active'])
    return redirect('listing', id=id)

@login_required
def add(request, id):
    obj = get_object_or_404(Listing, pk=id)
    instance, created = Watchlist.objects.get_or_create(user = request.user)
    instance.listing.add(obj) 
    messages.success(request, "Item added to watchlist successfully.")    
    return redirect('listing', id=id) 

def remove(request, id):
    obj = get_object_or_404(Listing, pk=id)
    instance, created = Watchlist.objects.get_or_create(user = request.user)
    instance.listing.remove(obj) 
    messages.error(request, "Item removed from watchlist successfully.")     
    return redirect('listing', id=id)

def categories(request):
    l = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "l" : l,
    })

def category(request, name):
    obj = get_object_or_404(Category, name=name)
    l = obj.listings.all()
    return render(request,"auctions/index.html",{
        "listings" : l,
        "tag" : name+" Category",
    })