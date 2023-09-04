from rest_framework import serializers
from .models import (
    AdsCategory,
    Advertisement,
    BotUser,
    AdsUser,
    TelegramGroupChannel
)


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'user_id', 'first_name', 'last_name', 'user_name', 'phone_number']


class AdsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsUser
        fields = ['id', 'user_id', 'user_name', 'user_link', 'phone_number']


class GroupChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramGroupChannel
        fields = ['id', 'chat_id', 'name', 'link', 'type']


class AdsSerializer(serializers.ModelSerializer):
    ads_user = AdsUserSerializer()
    group_channel = GroupChannelSerializer()

    class Meta:
        model = Advertisement
        fields = ['id', 'ads_user', 'categories', 'group_channel', 'message_id', 'message_text', 'datetime']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('product_len')

    def product_len(self, obj):
        count = 0
        if obj.subcategories.all():
            for subcat in obj.subcategories.all():
                count += subcat.advertisements.all().count()
        else:
            count += obj.advertisements.all().count()
        return count
    
    class Meta:
        model = AdsCategory
        fields = 'id', 'name', 'products'

