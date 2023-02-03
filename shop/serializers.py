from rest_framework import serializers
from .models import Category, Product


    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'category', 'name', 'image', 'description', 'price', 'status', 'created', 'updated'


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("category_name")

    class Meta:
        model = Category
        fields = 'id', 'parent', 'name'
    
    def category_name(self, category):
        lan = self.context.get("lan")
        name = category.name
        return name.get(lan)
        