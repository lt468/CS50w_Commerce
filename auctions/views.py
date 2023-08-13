from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max 
from decimal import Decimal

from django.utils.datastructures import MultiValueDictKeyError

from .models import User, Listing, Bid, Comment, WatchList, Category

def display_category(request, category):
    print(category)
    category_object = Category.objects.get(slug=category)
    items = Listing.objects.filter(category=category_object)

    return render(request, "auctions/display_category.html", {
        "category_title": category_object.category,
        "items": items
        })

def add_lisitng(request):
    # Checking to see if user has listed an item and then getting the information
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]
        start_bid_value = request.POST["start_bid_value"]
        image = request.FILES["image"]

        # Required to select correct category
        try:
            category_instance = Category.objects.get(category=category)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("index"))

        new_listing = Listing(item_title = title,
                              description = description,
                              category = category_instance,
                              starting_bid = start_bid_value,
                              owner = request.user,
                              item_image = image)

        new_listing.save()
        return HttpResponseRedirect(reverse('view_listing', args=[new_listing.item_id]))

    return render(request, "auctions/add_listing.html", {
        "categories": Category.objects.all()
        })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
        })

def view_listing(request, item_id):
    bid_made = None

    item = Listing.objects.get(pk=item_id)
    highest_bid = item.bids.aggregate(Max('bid_amount'))['bid_amount__max']
    if highest_bid is None:
        highest_bid = Decimal(item.starting_bid)

    # If the user clicks the add to watchlist button then there is a post but with no bid_value
    if request.method == "POST":
        try:
            new_bid = request.POST["bid_value"]
            if Decimal(new_bid) > Decimal(highest_bid):
                bid_made = True
            else:
                bid_made = False
        # Adding to watchlist
        except MultiValueDictKeyError:
            watchlist_entry = WatchList.objects.filter(user=request.user, item=item)
            if watchlist_entry.exists():
                watchlist_entry.delete()
            else:
                WatchList.objects.create(user=request.user, item=item)
            return HttpResponseRedirect(reverse('view_listing', args=[item_id]))

    # Check if the item is in the user's watchlist
    try:
        item_in_watchlist = WatchList.objects.filter(user=request.user, item=item).exists()
    except TypeError:
        item_in_watchlist = None

    return render(request, "auctions/view_listing.html", {
        "item": item,
        "highest_bid": highest_bid,
        "bid_made": bid_made,
        "item_in_watchlist": item_in_watchlist
        })

@login_required(login_url="login")
def watchlist(request):
    user = request.user
    watchlist_items = WatchList.objects.filter(user=user).select_related('item')

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
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
