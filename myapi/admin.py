from django.contrib import admin
from .models import User, Discount, Item, Purchase, PurchasedItem

# Register your models here.

admin.site.register(User)
admin.site.register(Discount)
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(PurchasedItem)
