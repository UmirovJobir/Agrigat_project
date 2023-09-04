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
    
    # def update(self, instance, validated_data):
    #     instance.message_id = validated_data.get('message_id', instance.message_id)
    #     instance.message_text = validated_data.get('message_text', instance.message_text)
    #     instance.datetime = validated_data.get('datetime', instance.datetime)
    #     instance.save()

    #     group_channel_data = validated_data.get('group_channel')
    #     print(group_channel_data)

    #     if group_channel_data:
    #         # try:
    #         #     group_channel = TelegramGroupChannel.objects.get(id=group_channel_data['chat_id'])
    #         # except:
    #         #     serializer = GroupChannelSerializer(data=group_channel_data)
    #         #     if serializer.is_valid():
    #         #         serializer.save()
    #         #         group_channel = TelegramGroupChannel.objects.get(id=serializer.data['id'])
    #         # instance.group_channel = group_channel

    #         group_channel_instance = instance.group_channel
    #         serializer = GroupChannelSerializer(group_channel_instance, data=group_channel_data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             # group_channel = TelegramGroupChannel.objects.get(id=serializer.data['id'])
    #         # instance.group_channel = group_channel
        
                
    #     categories = validated_data.get('categories', [])
    #     instance.categories.set(categories)

    #     return instance


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

