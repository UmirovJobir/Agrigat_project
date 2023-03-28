from rest_framework import serializers
from .models import Category, Product, User, ProductUser, KeyWords

    
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

class ProductSerializer(serializers.ModelSerializer):
    product_user = ProductUserSerializer()
    category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_user', 'category', 
            'group_id', 'group_name', 'group_link',
            'message_id', 'message_text', 'media_file', 
            'datatime', 'status'
        ]

    # Custom ProductUser()
    def create(self, validated_data):
        product_user_data = validated_data.get("product_user")

        product_user, created = ProductUser.objects.get_or_create(**product_user_data)
        
        product = Product.objects.create(product_user=product_user, **product_user_data)            

        return product_user





class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("category_name")

    class Meta:
        model = Category
        fields = 'id', 'parent', 'name'
    
    def category_name(self, category):
        lan = self.context.get("lan")
        name = category.name
        return name.get(lan)


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