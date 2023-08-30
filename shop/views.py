from django.views import generic
from django.utils import translation
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from shop.pagination import PaginationHandlerMixin

from .models import (
    BotUser,
    ProductUser,
    Category, 
    Product,  
    TelegramGroupChannel,
)
from .serializers import (
    BotUserSerializer,
    ProductUserSerializer,
    CategorySerializer, 
    ProductSerializer, 
)

def get_query_by_header(self, queryset):
    if 'HTTP_LAN' in self.request.META:
        lang = self.request.META['HTTP_LAN']
        translation.activate(lang)
    return queryset


class BotUserView(generics.ListCreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class ProductUserView(generics.ListCreateAPIView):
    queryset = ProductUser.objects.all()
    serializer_class = ProductUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ParentCategoryView(generics.ListAPIView):
    queryset = Category.objects.all().select_related('parent')
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(parent=None)
        queryset = get_query_by_header(self, queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubCategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all().select_related('parent')
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        parent_category_name = get_query_by_header(self, self.get_queryset().get(id=pk).name)
        subcategories = get_query_by_header(self, self.get_queryset().filter(parent=pk))
        serializer = self.get_serializer(subcategories, many=True)
        return Response({"parent_category_id": pk,
                         "parent_category_name": parent_category_name,  
                         "subcategories": serializer.data,})
            
            
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

      
class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().select_related('product_user', 'group_channel').prefetch_related('categories')

        chat_id = self.request.query_params.get('chat_id')
        message_id = self.request.query_params.get('message_id')

        if chat_id!=None and message_id!=None:
            queryset = queryset.filter(group_channel__chat_id=chat_id, message_id=message_id)
            
        return queryset


    def create(self, request, *args, **kwargs):
        group_channel, created_group = TelegramGroupChannel.objects.get_or_create(
            chat_id = request.data['group_channel']['chat_id'],
            name = request.data['group_channel']['name'],
            link = request.data['group_channel']['link'],)

        product_user, created_product = ProductUser.objects.get_or_create(
            user_id = request.data['product_user']['user_id'], 
            user_name = request.data['product_user']['user_name'],
            user_link = request.data['product_user']['user_link'],
            phone_number = request.data['product_user']['phone_number'],)

        try:
            product = Product.objects.get(product_user=product_user, message_text=request.data['message_text'])
            if product:
                product.group_channel = group_channel
                product.message_id = request.data['message_id']
                product.datetime = request.data['datetime']
                product.save()
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_302_FOUND)
            
        except (Product.DoesNotExist) as e:
            product = Product.objects.create(
                product_user = product_user,
                group_channel = group_channel,
                message_id = request.data['message_id'],
                message_text = request.data['message_text'],
                datetime = request.data['datetime'],
            )
            for category in request.data['categories']:
                product.categories.add(category)

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    # def delete(self, request):
    #     group_id = request.GET.get('group_id')
    #     message_id = request.GET.get('message_id')
        
    #     if (group_id!=None) and (message_id!=None):
    #         products = get_object_or_404(Product, group__group_id=group_id, message_id=message_id)
    #         products.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response(data={"error":"group_id and message_id is not given in params!"},status=status.HTTP_400_BAD_REQUEST)

    


class ProductDetailView(APIView):
    def get(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        product_serializer = ProductSerializer(products)
        return Response(product_serializer.data)

    def delete(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)

        group, created = Group.objects.get_or_create(
            group_id = request.data['group']['group_id'],
            group_name = request.data['group']['group_name'],
            group_link = request.data['group']['group_link'],
        )

        product.group = group
        product.message_id = request.data['message_id']
        product.message_text = request.data['message_text']
        product.media_file = request.data['media_file']
        product.datetime = request.data['datetime']

        categories = []
        for category_id in request.data.get('categories'):
            try:
                category = Category.objects.get(id=category_id)
                categories.append(category)
            except:
                return Response(data={"error":"Category id does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
        product.categories.set(categories)

        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        

class UpdateProductByGroupId(APIView):
    def patch(self, request, format=None):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        products = get_object_or_404(Product, group__group_id=group_id, message_id=message_id)
        serializer = ProductSerializer(products, data=request.data, partial=True)
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