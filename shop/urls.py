from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    UserView,
    ProductUserView,
    ProductUserDetailView,
    ParentCategoryView, 
    CategoryProductView,
    ProductView,
    ProductDetailView,
    KeyWordView,
    KeyWordsView,
)

urlpatterns = [
    path('user/', UserView.as_view()),
    
    path('product_user/', ProductUserView.as_view()),
    path('product_user/<int:pk>/', ProductUserDetailView.as_view()),

    path('keywords/', KeyWordsView.as_view()),
    path('keyword/', KeyWordView.as_view()),
    path('keyword/<int:pk>/', KeyWordView.as_view()),

    path('category/', ParentCategoryView.as_view()),
    path('category/<int:pk>/', CategoryProductView.as_view()),

    path('product/', ProductView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  