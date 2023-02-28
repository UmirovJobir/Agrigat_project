from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    username = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)
    link = models.URLField(max_length=500)  

    def __str__(self):
        return self.username

    class Meta:
        verbose_name='Bot user'
        verbose_name_plural='Bot users'


class ProductUser(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100)
    link = models.URLField(max_length=500)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name='Product user'
        verbose_name_plural='Product users'

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)
    name = models.JSONField(null=False, blank=False)

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

class Product(models.Model):
    product_user = models.ForeignKey(ProductUser, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    group_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=200)
    group_link = models.URLField(max_length=500)
    message_id = models.BigIntegerField(unique=True)
    message_text = models.TextField()
    media_file = models.FileField()
    datatime = models.DateTimeField()

    def __str__(self):
        return self.message_text
    
    class Meta:
        verbose_name='Product'
        verbose_name_plural='Products'

class KeyWords(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='key_words')
    key_words = models.JSONField()

    class Meta:
        verbose_name='Key word'
        verbose_name_plural='Key words'