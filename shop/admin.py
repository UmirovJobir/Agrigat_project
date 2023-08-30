import json
import pandas as pd
from django.forms import forms
from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.shortcuts import render
from modeltranslation.admin import TranslationAdmin
from .models import (
    BotUser,
    Category,
    Product,
    ProductUser,
    TelegramGroupChannel,
    UsefulCategory,
    UsefulCatalog,
)

admin.site.site_header = "Agrigat"
admin.site.site_title = "Agrigat bot portali"
admin.site.index_title = "Agrigat bot portaliga xush kelibsiz"


@admin.register(UsefulCategory)
class UsefulCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(UsefulCatalog)
class UsefulCatalogAdmin(admin.ModelAdmin):
    list_filter = ['type']


@admin.register(TelegramGroupChannel)
class TelegramGroupChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'name', 'link',]
    search_fields = ['chat_id',]


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_id']


@admin.register(ProductUser)
class ProductUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user_name', 'user_link', 'phone_number']
    list_display_links = ['user_id', 'user_name']
    search_fields = ['user_id', 'user_name', 'phone_number']


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name',]
    raw_id_fields = ['parent',]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_id', 'message_text', 'datetime']
    list_filter = ['group_channel',]
    search_fields = ['message_id', 'message_text']
    raw_id_fields = ['product_user','categories']
    list_per_page = 10




    
        