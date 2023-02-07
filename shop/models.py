from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import jsonfield

class User(models.Model):
    chat_id = models.PositiveBigIntegerField(unique=True, null=False, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    username = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)
    link = models.URLField(max_length = 200)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)
    name = models.JSONField() #models.CharField(max_length=2000) #

    
class Product(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products', null=False, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
