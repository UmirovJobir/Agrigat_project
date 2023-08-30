from django.db import models
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField


class BotUser(models.Model):
    user_id      = models.PositiveBigIntegerField(unique=True)
    first_name   = models.CharField(max_length=100, null=True, blank=True)
    last_name    = models.CharField(max_length=100, null=True, blank=True)
    user_name    = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name='Пользователь бота'
        verbose_name_plural='Пользователи бота'


class ProductUser(models.Model):
    user_id     = models.BigIntegerField(unique=True)
    user_name   = models.CharField(max_length=100)
    user_link   = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name='Пользователь продукта'
        verbose_name_plural='Пользователи продукта'


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
    
    def __str__(self) -> str:
        return self.name


class TelegramGroupChannel(models.Model):
    TYPE = (
        ('Group', 'Group'),
        ('Channel', 'Channel'),
    )
    chat_id = models.BigIntegerField()
    name    = models.CharField(max_length=200)
    link    = models.CharField(max_length=200, null=True, blank=True, unique=True)
    type    = models.CharField(max_length=20, choices=TYPE)

    def __str__(self):
        return f"{self.chat_id, self.name}"
    
    class Meta:
        verbose_name='Телеграм Группа или Канал'
        verbose_name_plural='Телеграм Группы или Каналы'


class Product(models.Model):
    product_user = models.ForeignKey(ProductUser, related_name='product_user', on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    group_channel = models.ForeignKey(TelegramGroupChannel, related_name='group_channel', on_delete=models.CASCADE, null=True, blank=True)
    message_id = models.BigIntegerField()
    message_text = models.TextField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        verbose_name='Продукт'
        verbose_name_plural='Продукты'


class UsefulCategory(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='useful_subcategories', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name='Полезная категория'
        verbose_name_plural='Полезные категории'


class UsefulCatalog(models.Model):
    TYPE = (
        ('Bot', 'Bot'),
        ('Group', 'Group'),
        ('Channel', 'Channel'),
        ('Website', 'Website'),
    )

    name     = models.CharField(max_length=200)
    link     = models.CharField(max_length=200, blank=True, unique=True)
    type     = models.CharField(max_length=20, choices=TYPE)
    category = models.ForeignKey(UsefulCategory, on_delete=models.CASCADE, related_name='useful_category', blank=True)

    class Meta:
        verbose_name='Полезный каталог'
        verbose_name_plural='Полезные каталоги'