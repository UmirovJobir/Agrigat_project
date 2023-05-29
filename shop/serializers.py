from rest_framework import serializers
from .models import Category, Product, User, KeyWords, ProductUser, Group
import json

def attempt_json_deserialize(data, expect_type=None):
    try:
        data = json.loads(data)
    except (TypeError, json.decoder.JSONDecodeError): pass

    if expect_type is not None and not isinstance(data, expect_type):
        raise ValueError(f"Got {type(data)} but expected {expect_type}.")

    return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'user_id', 'first_name', 
            'last_name', 'user_name', 
            'phone_number'
        ]


class ProductUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUser
        fields = 'id', 'user_id', 'user_name', 'user_link', 'phone_number'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','group_id', 'group_name', 'group_link',]

class ProductSerializer(serializers.ModelSerializer):
    product_user = ProductUserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'product_user', 'categories', 'group',
            'message_id', 'message_text', 'media_file', 
            'datetime'
        ]


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("category_name")
    products = serializers.SerializerMethodField('product_len')

    def product_len(self, category):
        categories = Category.objects.filter(parent=category.id).distinct()
        if len(categories)==0:
            products = Product.objects.filter(categories=category.id).select_related('product_user').prefetch_related('categories').distinct()
            return len(products)
        else:
            products = Product.objects.filter(categories__in=categories).select_related('product_user').prefetch_related('categories').distinct()
            if len(products)==0:
                categories_in = Category.objects.filter(parent__in=categories)
                products = Product.objects.filter(categories__in=categories_in).select_related('product_user').prefetch_related('categories').distinct()
            return len(products)
    
    def category_name(self, category):
        lan = self.context.get("lan")
        name = category.name
        return name.get(lan)
    
    class Meta:
        model = Category
        fields = 'id', 'name', 'products'

class KeyWordsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWords
        fields = 'category', 'key_words'    

class KeyWordsSerializer(serializers.ModelSerializer):
    key_words = serializers.SerializerMethodField("key")
    class Meta:
        model = KeyWords
        fields = 'id', 'category', 'key_words'
    
    def key(self, key_words):
        lan = self.context.get("lan")
        key_words = key_words.key_words
        return key_words.get(lan)