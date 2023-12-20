from django.contrib import admin
from .models import User, Shop, Item

# Register your models here.

admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Item)