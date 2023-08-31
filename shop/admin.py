from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from .admin_filter import AdsCategoryFilter
from .models import (
    User,
    Group,
    BotUser,
    AdsCategory,
    Advertisement,
    AdsUser,
    TelegramGroupChannel,
    UsefulCategory,
    UsefulCatalog,
)

admin.site.site_header = "Agrigat"
admin.site.site_title = "Agrigat bot portali"
admin.site.index_title = "Agrigat bot portaliga xush kelibsiz"

admin.site.register(User)
admin.site.register(Group)


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_id']


@admin.register(AdsUser)
class AdsUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user_name', 'user_link', 'phone_number']
    list_display_links = ['user_id', 'user_name']
    search_fields = ['user_id', 'user_name', 'phone_number']


@admin.register(AdsCategory)
class AdsCategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name',]
    raw_id_fields = ['parent',]


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_id', 'message_text', 'datetime']
    list_filter = ['group_channel',]
    search_fields = ['message_id', 'message_text']
    raw_id_fields = ['ads_user','categories']
    list_per_page = 10


@admin.register(TelegramGroupChannel)
class TelegramGroupChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'name', 'link',]
    search_fields = ['chat_id',]


@admin.register(UsefulCategory)
class UsefulCategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    list_filter = [AdsCategoryFilter]
    search_fields = ['name']

@admin.register(UsefulCatalog)
class UsefulCatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_website_link', 'type', 'category']
    list_display_links = ['id', 'name']

    def display_website_link(self, obj):
        if obj.link[0]=="@":
            return format_html('<a href="https://t.me/{0}" target="_blank">@{0}</a>', obj.link[1:])
        elif obj.link[0:4]=="http":
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.link)

    display_website_link.short_description = 'Website Link'

    
        