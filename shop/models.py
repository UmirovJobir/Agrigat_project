from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    user_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    user_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.username

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


class Product(models.Model):
    product_user = models.ForeignKey(ProductUser, related_name='product_user', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='category', blank=True)
    group_id = models.BigIntegerField()
    group_name = models.CharField(max_length=200)
    group_link = models.CharField(max_length=200, null=False, blank=False)
    message_id = models.BigIntegerField(unique=True)
    message_text = models.TextField()
    media_file = models.TextField()
    datatime = models.IntegerField()
    status = models.BooleanField()

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
