from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    image = models.URLField(max_length=500, blank=True)
    c = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self,*args,**kwargs): 
        if not self.current_bid:
            self.current_bid = self.starting_bid           
        super(Listing,self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.title} ({self.starting_bid})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    listings = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.name}"

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()

class comments(models.Model):
    comment = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.writer} {self.listing.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing, related_name="Listings")

    def __str__(self):
        return f"{self.user} Watchlist"
