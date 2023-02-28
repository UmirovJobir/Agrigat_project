from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import (
    Category, 
    Product, 
    User, 
    KeyWords)
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    UserSerializer, 
    KeyWordsSerializer)


class KeyWordsView(APIView):
    def get(self, request):
        lan = request.META['HTTP_LAN']
        key_words = KeyWords.objects.all()
        serializer = KeyWordsSerializer(
            key_words, 
            many=True, 
            context={'lan': lan}
            )
        return Response(serializer.data)

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


class ParentCategoryView(APIView):
    def get(self, request):
        lan = request.META['HTTP_LAN']
        categories = Category.objects.filter(parent=None)
        products = Product.objects.all()
        category_serializer = CategorySerializer(
            categories, 
            many=True, 
            context={'lan': lan}
            )
        product_serializer = ProductSerializer(products, many=True)
        return Response(data={
            "categories":category_serializer.data, 
            "products":product_serializer.data}
            )


class CategoryProductView(APIView):
    def get(self, request, pk: int):
        lan = request.META['HTTP_LAN']
        categories = Category.objects.filter(parent=pk)
        if len(categories)==0:
            products = Product.objects.filter(category=pk).select_related('category')
        else:
            products = Product.objects.filter(category__in=categories).select_related('category')
            if len(products)==0:
                categories_in = Category.objects.filter(parent__in=categories)
                products = Product.objects.filter(category__in=categories_in).select_related('category')
        product_serializer = ProductSerializer(products, many=True)
        category_serializer = CategorySerializer(
            categories, 
            many=True, 
            context={'lan': lan}
            )
        product_count = len(products)
        return Response(data={
            "categories":category_serializer.data, 
            "product_count":product_count,
            "products":product_serializer.data}
            )
            
        
class ProductView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
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

class ProductDetailView(APIView):
    def get(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        product_serializer = ProductSerializer(products)
        return Response(product_serializer.data)

    def delete(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        


