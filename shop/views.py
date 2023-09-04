from django.views import generic
from django.utils import translation
from django.shortcuts import get_object_or_404 

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination

from shop.pagination import CustomPageNumberPagination

from .models import (
    BotUser,
    AdsUser,
    AdsCategory, 
    Advertisement,  
    TelegramGroupChannel,
)
from .serializers import (
    BotUserSerializer,
    AdsUserSerializer,
    CategorySerializer, 
    AdsSerializer,
    GroupChannelSerializer
)

def get_query_by_header(self, queryset):
    if 'HTTP_LAN' in self.request.META:
        lang = self.request.META['HTTP_LAN']
        translation.activate(lang)
    return queryset


class BotUserView(generics.ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class AdsUserView(generics.ListCreateAPIView):
    queryset = AdsUser.objects.all()
    serializer_class = AdsUserSerializer


class ParentCategoryView(generics.ListAPIView):
    queryset = AdsCategory.objects.all().select_related('parent')
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(parent=None)
        queryset = get_query_by_header(self, queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubCategoryView(generics.RetrieveAPIView):
    queryset = AdsCategory.objects.all().select_related('parent')
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        parent_category_name = get_query_by_header(self, self.get_queryset().get(id=pk).name)
        subcategories = get_query_by_header(self, self.get_queryset().filter(parent=pk))
        serializer = self.get_serializer(subcategories, many=True)
        return Response({"parent_category_id": pk,
                         "parent_category_name": parent_category_name,  
                         "subcategories": serializer.data,})

   
class AdsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AdsSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Advertisement.objects.all().select_related('ads_user', 'group_channel').prefetch_related('categories')
        chat_id = self.request.query_params.get('chat_id')
        message_id = self.request.query_params.get('message_id')
        if chat_id!=None and message_id!=None:
            queryset = queryset.filter(group_channel__chat_id=chat_id, message_id=message_id)
        return queryset


    def create(self, request, *args, **kwargs):
        group_channel = TelegramGroupChannel.objects.filter(
                        chat_id = request.data.get('group_channel')['chat_id'],
                        link    = request.data.get('group_channel')['link']).first()
        if group_channel==None:
            serializer = GroupChannelSerializer(data=request.data.get('group_channel'))
            if serializer.is_valid():
                serializer.save()
                group_channel = TelegramGroupChannel.objects.get(id=serializer.data['id'])
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('ads_user'):
            ads_user = AdsUser.objects.filter(
                            user_id   = request.data.get('ads_user')['user_id'], 
                            user_link = request.data.get('ads_user')['user_link']).first()
            if ads_user==None:
                ads_user = AdsUser.objects.create(
                    user_id      = request.data.get('ads_user')['user_id'], 
                    user_name    = request.data.get('ads_user')['user_name'],
                    user_link    = request.data.get('ads_user')['user_link'],
                    phone_number = request.data.get('ads_user')['phone_number'])
        try:
            advertisement = Advertisement.objects.get(ads_user=ads_user, message_text=request.data.get('message_text'))
            advertisement.group_channel = group_channel
            advertisement.message_id = request.data.get('message_id')
            advertisement.datetime = request.data.get('datetime')
            advertisement.save()
            serializer = AdsSerializer(advertisement)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except (Advertisement.DoesNotExist) as e:
            advertisement = Advertisement.objects.create(
                ads_user = ads_user,
                group_channel = group_channel,
                message_id = request.data['message_id'],
                message_text = request.data['message_text'],
                datetime = request.data['datetime'])
            
            for category in request.data['categories']:
                advertisement.categories.add(category)

            serializer = AdsSerializer(advertisement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdsRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = AdsSerializer
    queryset = Advertisement.objects.all() \
                .select_related('ads_user', 'group_channel') \
                .prefetch_related('categories')
    

class AdvertisementDeleteView(APIView):
    def delete(self, request):
        group_channal_id = request.GET.get('group_channal_id')
        message_id = request.GET.get('message_id')
        
        if group_channal_id and message_id:
            products = get_object_or_404(Advertisement, group_channel__chat_id=group_channal_id, message_id=message_id)
            products.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"error":"group_id and message_id is not given in params!"},status=status.HTTP_400_BAD_REQUEST)


class AdvertisementPatchView(APIView):
    def patch(self, request, pk, format=None):
        product = get_object_or_404(Advertisement, pk=pk)
        
        if request.data.get('group_channel'):
            group_channel = TelegramGroupChannel.objects.filter(
                            chat_id = request.data.get('group_channel')['chat_id'],
                            link    = request.data.get('group_channel')['link']).first()
            if group_channel==None:
                serializer = GroupChannelSerializer(data=request.data.get('group_channel'))
                if serializer.is_valid():
                    serializer.save()
                    group_channel = TelegramGroupChannel.objects.get(id=serializer.data['id'])
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            product.group_channel = group_channel

        if request.data.get('message_id'):
            product.message_id = request.data.get('message_id')
        if request.data.get('message_text'):
            product.message_text = request.data.get('message_text')
        if request.data.get('datetime'):
            product.datetime = request.data.get('datetime')

        categories = []
        for category_id in request.data.get('categories'):
            try:
                category = AdsCategory.objects.get(id=category_id)
                categories.append(category)
            except:
                return Response(data={"error":"Category id does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
        product.categories.set(categories)
        product.save()
        serializer = AdsSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        

class AdsUpdateByGroupId(APIView):
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        message_id = request.GET.get('message_id')
        advertisements = get_object_or_404(Advertisement, group_channel__chat_id=chat_id, message_id=message_id)
        serializer = AdsSerializer(advertisements)
        return Response(serializer.data)
        

    def patch(self, request, format=None):
        chat_id = request.GET.get('chat_id')
        message_id = request.GET.get('message_id')
        advertisements = get_object_or_404(Advertisement, group_channel__chat_id=chat_id, message_id=message_id)
        serializer = AdsSerializer(advertisements, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#webappbot
class IndexViewWebAppBot(generic.ListView):
    model = BotUser
    template_name = 'index.html'

#example
class IndexViewExample(generic.ListView):
    model = BotUser
    template_name = 'example.html'