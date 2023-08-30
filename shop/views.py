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


class OnlyCategory(APIView):
    def get(self, request):
        category_id = self.request.query_params.get("id")
    
        if category_id=='' or category_id==None:
            categories = Category.objects.filter(parent=None)
        else:
            categories = Category.objects.filter(parent=category_id)
        
        queryset = get_query_by_header(self, categories)
        category_serializer = CategorySerializer(queryset, many=True)

        if category_id=='':
            return Response(data={"categories": category_serializer.data,})
        else:
            category_name = Category.objects.get(id=category_id)
            
            try:
                parent_id = category_name.parent.id
            except AttributeError:
                parent_id = None

            return Response(data={
                "parent_id": parent_id,
                "categories": category_serializer.data,}
                )
    
    # def get(self, request):
    #     try:
    #         lan = request.META['HTTP_LAN']
    #     except:
    #         return Response(
    #         data={"error": "lan does not exist!"}, 
    #         status=status.HTTP_400_BAD_REQUEST
    #         )
    #     category_id = self.request.query_params.get("id")
        
    #     if category_id is None:
    #         return Response(data={"error":"query_params is not given"}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         if category_id=='':
    #             categories = Category.objects.filter(parent=None)
    #         else:
    #             categories = Category.objects.filter(parent=category_id)
                
    #         category_serializer = CategorySerializer(categories, many=True, context={'lan': lan})

    #         if category_id=='':
    #             return Response(data={"categories": category_serializer.data,})
    #         else:
    #             category_name = Category.objects.get(id=category_id)
                
    #             try:
    #                 parent_id = category_name.parent.id
    #             except AttributeError:
    #                 parent_id = None

    #             return Response(data={
    #                 "parent_id": parent_id,
    #                 "category_name":category_name.name[f'{lan}'],
    #                 "categories": category_serializer.data,}
    #                 )
            
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class ParentCategoryView(generics.ListAPIView):    
    pagination_class = BasicPagination
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True).select_related('parent')
        return get_query_by_header(self, queryset)


    # def get(self, request, format=None, *args, **kwargs):
    #     categories = Category.objects.filter(parent=None).select_related('parent')
    #     queryset = get_query_by_header(self, categories)
    #     category_serializer = CategorySerializer(queryset, many=True)
    #     return Response(category_serializer.data)

        # try:
        #     lan = request.META['HTTP_LAN']
        # except:
        #     return Response(
        #     data={"error": "lan does not exist!"}, 
        #     status=status.HTTP_400_BAD_REQUEST
        #     )

        # categories = Category.objects.filter(parent=None).select_related('parent')
        # category_serializer = CategorySerializer(categories, many=True, context={'lan': lan,})

        # products = Product.objects.all().select_related('product_user').prefetch_related('categories')
        # page = self.paginate_queryset(products)

        # if page is not None:
        #     product_serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        # else:
        #     product_serializer = self.serializer_class(products, many=True)
        
        # return Response(data={
        #                 "categories":category_serializer.data, 
        #                 "products":product_serializer.data,
        #                 }, status=status.HTTP_200_OK)


class CategoryProductView(APIView):
    def get(self, request, pk: int):
        try:
            lan = request.META['HTTP_LAN']
        except:
            return Response(
            data={"error": "lan does not exist!"}, 
            status=status.HTTP_400_BAD_REQUEST
            )
        
        category_name = Category.objects.get(id=pk).name[f'{lan}']

        categories = Category.objects.filter(parent=pk)
        if len(categories)==0:
            products = Product.objects.filter(category=pk).select_related('product_user').distinct()
        else:
            products = Product.objects.filter(category__in=categories).select_related('product_user').distinct()
            if len(products)==0:
                categories_in = Category.objects.filter(parent__in=categories)
                products = Product.objects.filter(category__in=categories_in).select_related('product_user').distinct()
        product_serializer = ProductSerializer(products, many=True)

        
        category_serializer = CategorySerializer(categories, many=True)
        return Response(data={
                        "category_name":category_name,
                        "categories":category_serializer.data, 
                        "product_count":len(products),
                        "products":product_serializer.data}
                        )

      
class ProductView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = ProductSerializer

    def get(self, request):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        
        if (group_id==None) and (message_id==None):
            products = Product.objects.all().select_related('product_user').prefetch_related('categories__parent').order_by('-id')
            page = self.paginate_queryset(products)

            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(products, many=True)
        else:
            products = get_object_or_404(Product, group__group_id=group_id, message_id=message_id)
            serializer = ProductSerializer(products)
        return Response(serializer.data)

    def delete(self, request):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        
        if (group_id!=None) and (message_id!=None):
            products = get_object_or_404(Product, group__group_id=group_id, message_id=message_id)
            products.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"error":"group_id and message_id is not given in params!"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        group, created_group = Group.objects.get_or_create(
            group_id = request.data['group']['group_id'],
            group_name = request.data['group']['group_name'],
            group_link = request.data['group']['group_link'],
        )

        product_user, created_product = ProductUser.objects.get_or_create(
            user_id = request.data['product_user']['user_id'], 
            user_name = request.data['product_user']['user_name'],
            user_link = request.data['product_user']['user_link'],
            phone_number = request.data['product_user']['phone_number'],
        )


        try:
            product = Product.objects.get(product_user=product_user, message_text=request.data['message_text'])

            if product:
                product.group = group
                product.message_id = request.data['message_id']
                product.datetime = request.data['datetime']
                product.save()
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_302_FOUND)
            
        except (Product.DoesNotExist) as e:
            product = Product.objects.create(
                product_user = product_user,
                group = group,
                message_id = request.data['message_id'],
                message_text = request.data['message_text'],
                media_file = request.data['media_file'],
                datetime = request.data['datetime'],
            )
            for category in request.data['categories']:
                product.categories.add(category)

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            


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