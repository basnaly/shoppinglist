from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}, {self.first_name}, {self.last_name}, {self.email}"
    
    
class Shop(models.Model):
    shop_name = models.CharField(max_length=2056)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    
    def __str__(self):
        return f"{self.shop_name}, {self.owner}"
    
    
class Item(models.Model):
    item_name = models.CharField(max_length=256)
    item_note = models.CharField(max_length=2056, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shops")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    
    def __str__(self):
        return f"{self.item_name}, {self.item_note}, {self.shop}, {self.owner}"
    
    