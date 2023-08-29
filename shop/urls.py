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
    UpdateProductByGroupId,
    IndexViewWebAppBot,
    IndexViewExample
)
from util.chart import get_months, get_days, get_products_len_in_a_day_by_groups


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

    path('update_by_group_id/', UpdateProductByGroupId.as_view()),
    
    path("get_months/", get_months, name="get-months"),
    path("get_days/<int:month>", get_days, name="get-days"),
    path("get_groups_products/<int:month>/<int:day>/", get_products_len_in_a_day_by_groups, name="get-groups-products"),
    path('webappbot/', IndexViewWebAppBot.as_view(), name='index'),
    path('example/', IndexViewExample.as_view(), name='example'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  