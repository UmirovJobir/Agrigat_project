from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from shop.pagination import PaginationHandlerMixin
import json
import math
from .models import (
    User,
    ProductUser,
    Category, 
    Product,  
    KeyWords)
from .serializers import (
    UserSerializer,
    ProductUserSerializer,
    CategorySerializer, 
    ProductSerializer, 
    KeyWordsSerializer,
    KeyWordsPostSerializer,
    )


class UserView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

class ProductUserView(APIView):
    def get(self, request):
        user = ProductUser.objects.all()
        serializer = ProductUserSerializer(user, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        user_id = request.data["user_id"]
        try:
            ProductUser.objects.get(user_id = user_id)
            return Response(
                    data={"error": "user_id is exist"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ProductUser.DoesNotExist:
            serializer = ProductUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )


class OnlyCategory(APIView):
    def get(self, request):
        try:
            lan = request.META['HTTP_LAN']
        except:
            return Response(
            data={"error": "lan does not exist!"}, 
            status=status.HTTP_400_BAD_REQUEST
            )
        category_id = self.request.query_params.get("id")
        
        if category_id is None:
            return Response(data={"error":"query_params is not given"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if category_id=='':
                categories = Category.objects.filter(parent=None)
            else:
                categories = Category.objects.filter(parent=category_id)
                
            category_serializer = CategorySerializer(categories, many=True, context={'lan': lan})

            if category_id=='':
                return Response(data={"categories": category_serializer.data,})
            else:
                category_name = Category.objects.get(id=category_id).name[f'{lan}']
                return Response(data={
                    "category_name":category_name,
                    "categories": category_serializer.data,}
                    )
            
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class ParentCategoryView(APIView, PaginationHandlerMixin):    
    pagination_class = BasicPagination
    serializer_class = ProductSerializer


    def get(self, request, format=None, *args, **kwargs):
        try:
            lan = request.META['HTTP_LAN']
        except:
            return Response(
            data={"error": "lan does not exist!"}, 
            status=status.HTTP_400_BAD_REQUEST
            )

        categories = Category.objects.filter(parent=None).select_related('parent')
        category_serializer = CategorySerializer(categories, many=True, context={'lan': lan,})

        products = Product.objects.all().select_related('product_user').prefetch_related('category__parent')
        page = self.paginate_queryset(products)

        if page is not None:
            product_serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            product_serializer = self.serializer_class(products, many=True)
        
        return Response(data={
                        "categories":category_serializer.data, 
                        "products":product_serializer.data,
                        }, status=status.HTTP_200_OK)


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

        
        category_serializer = CategorySerializer(categories, many=True, context={'lan': lan})
        return Response(data={
                        "category_name":category_name,
                        "categories":category_serializer.data, 
                        "product_count":len(products),
                        "products":product_serializer.data}
                        )


class KeyWordIDView(APIView):
    def get(self, request, pk: int):
        lan = request.META['HTTP_LAN']
        key_words = KeyWords.objects.filter(category=pk)
        serializer = KeyWordsSerializer(
            key_words, 
            many=True, 
            context={'lan': lan}
            )
        data = serializer.data
        data = json.loads(json.dumps(data))
        response = []
        for i in data:
            if i['key_words'] != None:
                response.append(i)
        return Response(response)

class CheckKeywordByWord(APIView):
    def get(self, request):
        lan = request.META['HTTP_LAN']
        word = self.request.query_params.get("word")
        key_words = KeyWords.objects.filter(key_words={lan:word})
        serializer = KeyWordsSerializer(
            key_words, 
            many=True, 
            context={'lan': lan}
            )
        data = serializer.data
        data = json.loads(json.dumps(data))
        response = []
        for i in data:
            if i['key_words'] != None:
                response.append(i)
        return Response(response)

class KeyWordView(APIView):
    def post(self, request):
        try:
            lan = request.META['HTTP_LAN']
        except:
            return Response(
            data={"error": "lan does not exist!"}, 
            status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        data = json.loads(json.dumps(data))
        data['key_words'] = {lan:data['key_words']}
        serializer = KeyWordsPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

      
class ProductView(APIView):
    def get(self, request):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        
        if (group_id==None) and (message_id==None):
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        else:
            products = get_object_or_404(Product, group_id=group_id, message_id=message_id)
            serializer = ProductSerializer(products)
        return Response(serializer.data)

    def delete(self, request):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        
        if (group_id!=None) and (message_id!=None):
            products = get_object_or_404(Product, group_id=group_id, message_id=message_id)
            products.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"error":"group_id and message_id is not given in params!"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        product_serializer = ProductSerializer(products)
        return Response(product_serializer.data)

    def delete(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        products = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class UpdateProductByGroupId(APIView):
    def put(self, request, format=None):
        group_id = request.GET.get('group_id')
        message_id = request.GET.get('message_id')
        products = get_object_or_404(Product, group_id=group_id, message_id=message_id)
        serializer = ProductSerializer(products, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
