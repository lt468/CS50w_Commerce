import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

def user_media_path(instance, filename):
    # Get the user's id
    user_id = instance.owner.id

    # Create a subdirectory using the user's id
    upload_path = os.path.join(str(user_id), filename)

    return upload_path

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, default='default-slug')  # Creates a slug for the url

    # Makes the slug
    def save(self):
        self.slug = slugify(self.category)  # Generate slug from category
        super().save()
    
    def __str__(self):
        return self.category

class Listing(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="classification")
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    item_image = models.ImageField(upload_to=user_media_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_title} by {self.owner}, id {self.item_id}"

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_lister")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"bid id: {self.bid_id} on {self.item} by {self.bidder} for £{self.bid_amount} at {self.bid_time}"

class HighestBid(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="highest_bid")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comment")
    # When a commenter, a user, is deleted then all their comments are deleted too
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment id: {self.comment_id} by {self.commenter} on {self.comment_item}"

class WatchList(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="favourite")

    def __str__(self):
        return f"{self.item} watched by {self.user}"

