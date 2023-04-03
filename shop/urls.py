from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    UserView,
    ProductUserView,
    OnlyCategory,
    ParentCategoryView, 
    CategoryProductView,
    ProductView,
    ProductDetailView,
    KeyWordView,
    KeyWordIDView,
    CheckKeywordByWord,
    Test
)

urlpatterns = [
    path('user/', UserView.as_view()),
    path('product_user/', ProductUserView.as_view()),
    
    path('keyword/', KeyWordView.as_view()),
    path('keyword_id/<int:pk>/', KeyWordIDView.as_view()),
    
    path('check_keyword/', CheckKeywordByWord.as_view()),

    path('catagory_name/', OnlyCategory.as_view()),
    path('category/', ParentCategoryView.as_view()),
    path('category/<int:pk>/', CategoryProductView.as_view()),

    path('product/', ProductView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),

    path('test/', Test.as_view())
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  