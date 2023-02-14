from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

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
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)