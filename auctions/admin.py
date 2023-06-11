from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(comments)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Category)