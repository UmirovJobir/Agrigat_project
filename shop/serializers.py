from rest_framework import serializers
import json
from .models import (
    Category,
    Product,
    BotUser,
    ProductUser,
    TelegramGroupChannel
)

# def attempt_json_deserialize(data, expect_type=None):
#     try:
#         data = json.loads(data)
#     except (TypeError, json.decoder.JSONDecodeError): pass

#     if expect_type is not None and not isinstance(data, expect_type):
#         raise ValueError(f"Got {type(data)} but expected {expect_type}.")

#     return data

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'user_id', 'first_name', 'last_name', 'user_name', 'phone_number']


class ProductUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUser
        fields = ['id', 'user_id', 'user_name', 'user_link', 'phone_number']


class GroupChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramGroupChannel
        fields = ['id', 'chat_id', 'name', 'link', 'type']


class ProductSerializer(serializers.ModelSerializer):
    product_user = ProductUserSerializer()
    group = GroupChannelSerializer()

    class Meta:
        model = Product
        fields = ['id', 'product_user', 'categories', 'group_channel', 'message_id', 'message_text', 'datetime']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('product_len')

    def product_len(self, obj):
        print(obj.products.all().count())
        return f'{obj}'
    
        # categories = Category.objects.filter(parent=category.id).distinct()
        # if len(categories)==0:
        #     products = Product.objects.filter(categories=category.id).select_related('product_user').prefetch_related('categories').distinct()
        #     return len(products)
        # else:
        #     products = Product.objects.filter(categories__in=categories).select_related('product_user').prefetch_related('categories').distinct()
        #     if len(products)==0:
        #         categories_in = Category.objects.filter(parent__in=categories)
        #         products = Product.objects.filter(categories__in=categories_in).select_related('product_user').prefetch_related('categories').distinct()
        #     return len(products)

    
    class Meta:
        model = Category
        fields = 'id', 'name', 'products'

