from django.contrib.auth.models import AbstractUser
from django.db import models

def user_media_path(instance, fname):
    return "media/pencil.jpg"

# In your view or form where you handle the file uploads, you can use this media path generation function like this:
#uploaded_file = request.FILES['file']  # Replace 'file' with the actual field name
#user_id = request.user.id
#media_path = user_media_path(request.user, uploaded_file.name)
#
## Save the uploaded file to the media path
#with open(media_path, 'wb') as f:
#    for chunk in uploaded_file.chunks():
#        f.write(chunk)

class User(AbstractUser):
    pass

class Listing(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    item_image = models.ImageField(upload_to=user_media_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    time = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_lister")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    bid_time = models.DateTimeField(auto_now_add=True)

class HighestBid(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="highest_bid")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    # When a commenter, a user, is deleted then all their comments are deleted too
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    comment_time = models.DateTimeField(auto_now_add=True)

class WatchList(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="favourite")

