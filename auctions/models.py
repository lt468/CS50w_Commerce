from django.contrib.auth.models import AbstractUser - cons
from django.db import models

def user_media_path(instance, fname):
    return f"user_{instance.id}/{fname}"

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

class Listings(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=64)
    description = models.TextField()
    # There must always be a starting bid price
    starting_bid = models.DecimalField(max_digits=None, decimal_places=2, default=0.01)
    current_bid = models.DecimalField(max_digits=None, decimal_places=2, default=0.01)
    category = models.CharField(max_length=64)
    item_image = models.ImageField(upload_to=user_media_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    bid_amount = models.DecimalField(max_digits=None, decimal_places=2, default=0.01)
    bid_time = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    # When a commenter, a user, is deleted then all their comments are deleted too
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    comment_time = models.DateTimeField(auto_now_add=True)

