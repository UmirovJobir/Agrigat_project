from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


class User(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    user_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name='Bot user'
        verbose_name_plural='Bot users'


class ProductUser(models.Model):
    user_id = models.BigIntegerField()
    user_name = models.CharField(max_length=100)
    user_link = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name='Product user'
        verbose_name_plural='Product users'


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)
    name = models.JSONField(null=False, blank=False)
    
    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'


class Group(models.Model):
    group_id = models.BigIntegerField()
    group_name = models.CharField(max_length=200)
    group_link = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.group_id, self.group_name}"
    
    class Meta:
        verbose_name='Group'
        verbose_name_plural='Groups'


class Product(models.Model):
    product_user = models.ForeignKey(ProductUser, related_name='product_user', on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='category', blank=True)
    group = models.ForeignKey(Group, related_name='group', on_delete=models.CASCADE, null=True, blank=True)
    message_id = models.BigIntegerField()
    message_text = models.TextField()
    media_file = models.TextField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return self.message_text
    
    class Meta:
        verbose_name='Product'
        verbose_name_plural='Products'


class KeyWords(models.Model):
    category = models.IntegerField()
    key_words = models.JSONField()

    class Meta:
        verbose_name='Key word'
        verbose_name_plural='Key words'
