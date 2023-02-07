from rest_framework import serializers
from .models import Category, Product, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'chat_id', 'first_name', 'last_name', 'username', 'phone_number', 'link'
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'category', 'name', 'image', 'description', 'price', 'created', 'updated'


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("category_name")

    class Meta:
        model = Category
        fields = 'id', 'parent', 'name'
    
    def category_name(self, category):
        lan = self.context.get("lan")
        name = category.name
        print(name.get(lan))
        return name.get(lan)
        