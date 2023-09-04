from django.db import models
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, User


class User(User):
    pass

    class Meta:
        app_label = 'shop'
        verbose_name=_("Adminstrator") #('Пользователь бота')
        verbose_name_plural=_("Adminstratorlar") #('Пользователи бота')

class Group(Group):
    pass

    class Meta:
        app_label = 'shop'
        verbose_name=_("Adminstratorlar guruhi") #('Пользователь бота')
        verbose_name_plural=_("Adminstratorlar guruhi") #('Пользователи бота')

class BotUser(models.Model):
    user_id      = models.PositiveBigIntegerField(unique=True)
    first_name   = models.CharField(max_length=100, null=True, blank=True)
    last_name    = models.CharField(max_length=100, null=True, blank=True)
    user_name    = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name=_("Bot foydalanuvchisi") #('Пользователь бота')
        verbose_name_plural=_("Bot foydalanuvchilari") #('Пользователи бота')


class AdsUser(models.Model):
    user_id     = models.BigIntegerField(unique=True)
    user_name   = models.CharField(max_length=100)
    user_link   = models.CharField(max_length=100, null=True, blank=True, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name=_("E'lon foydalanuvchisi") #('Пользователь продукта')
        verbose_name_plural=_("E'lon foydalanuvchilari")


class AdsCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    name   = models.CharField(max_length=100)
    
    class Meta:
        verbose_name=_("E'lon toifasi") #('Категория')
        verbose_name_plural=_("E'lon toifalari") #('Категории')
    
    def __str__(self) -> str:
        return self.name


class TelegramGroupChannel(models.Model):
    TYPE = (
        ('Group', _('Gruppa')),
        ('Channel', _('Kanal')),
    )
    chat_id = models.BigIntegerField(unique=True)
    name    = models.CharField(max_length=200)
    link    = models.CharField(max_length=200, null=True, blank=True, unique=True)
    type    = models.CharField(max_length=20, choices=TYPE)

    def __str__(self):
        return f"{self.chat_id, self.name}"
    
    class Meta:
        verbose_name=_("Telegram gruppa/kanal") #('Телеграм Группа или Канал')
        verbose_name_plural=_("Telegram gruppalar/kanallar")


class Advertisement(models.Model):
    ads_user = models.ForeignKey(AdsUser, related_name='ads_user'   , on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(AdsCategory, related_name='advertisements', blank=True)
    group_channel = models.ForeignKey(TelegramGroupChannel, related_name='group_channel', on_delete=models.CASCADE, null=True, blank=True)
    message_id = models.BigIntegerField()
    message_text = models.TextField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name=_("E'lon") #('Продукт')
        verbose_name_plural=_("E'lonlar") #('Продукты')


class UsefulCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='useful_subcategories', null=True, blank=True)
    name   = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name=_("Foydali toifa") #('Полезная категория')
        verbose_name_plural=_("Foydali toifalar") #('Полезные категории')


class UsefulCatalog(models.Model):
    TYPE = (
        ('Bot', _('Bot')),
        ('Group', _('Gruppa')),
        ('Channel', _('Kanal')),
        ('Website', _('Websayt')),
    )

    name     = models.CharField(max_length=200)
    link     = models.CharField(max_length=200, blank=True, unique=True)
    type     = models.CharField(max_length=20, choices=TYPE)
    category = models.ForeignKey(UsefulCategory, on_delete=models.CASCADE, related_name='useful_category', blank=True)

    class Meta:
        verbose_name=_("Foydali manba") #('Полезный каталог')
        verbose_name_plural=_("Foydali manbalar") #('Полезные каталоги')