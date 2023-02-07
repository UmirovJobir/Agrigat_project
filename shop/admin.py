from django.contrib import admin
from .models import User, Category, Product
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'chat_id', 'link')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    # raw_id_fields = ('parent',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
    list_display = ('name', 'price', 'user')
    list_filter = ('category__id','user')
    search_fields = ('category__name','name','user','price')


    
        