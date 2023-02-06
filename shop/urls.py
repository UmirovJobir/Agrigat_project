from django.urls import path
from .views import (
    ParentCategoryView, 
    CategoryProductView,
    ProductView,
    ProductDetailView,
    UserView,
)

urlpatterns = [
    path('user/', UserView.as_view()),
    path('category/', ParentCategoryView.as_view()),
    path('category/<int:pk>/', CategoryProductView.as_view()),
    path('product/', ProductView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
]