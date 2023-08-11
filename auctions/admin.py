from django.contrib import admin
from .models import User, Listing, Bid, Comment, WatchList, HighestBid, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(HighestBid)
admin.site.register(Category)
