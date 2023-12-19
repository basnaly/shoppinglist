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