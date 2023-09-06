from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    BotUserView,
    AdsUserView,
    ParentCategoryView,
    SubCategoryView,
    ParentCategoryView,

    AdsListCreateAPIView,
    AdsRetrieveDestroyAPIView,
    AdvertisementDeleteView,
    AdvertisementPatchView,

    AdsUpdateByGroupId,

    UsefulCategoryListAPIView,
    UsefulSubCategoryView,
    UsefulCatalogAPIView,
    UsefulCatalogDetailAPIView,

    IndexViewWebAppBot,
    IndexViewExample
)
from util.chart import get_months, get_days, get_products_len_in_a_day_by_groups


urlpatterns = [
    path('user/', BotUserView.as_view()),
    path('ads_user/', AdsUserView.as_view()),
    
    path('category/', ParentCategoryView.as_view()),
    path('category/<int:pk>/', SubCategoryView.as_view()),

    path('advertisement/', AdsListCreateAPIView.as_view()),
    path('advertisement/<int:pk>/', AdsRetrieveDestroyAPIView.as_view()),
    path('advertisement/<int:pk>/update/', AdvertisementPatchView.as_view()),
    path('advertisement_delete/', AdvertisementDeleteView.as_view()),
    path('advertisement_chat_id/', AdsUpdateByGroupId.as_view()),

    path('usefulcategory/', UsefulCategoryListAPIView.as_view()),
    path('usefulcategory/<int:pk>/', UsefulSubCategoryView.as_view()),

    path('usefulcategory/<int:pk>/usefulcatalog/', UsefulCatalogAPIView.as_view()),
    path('usefulcatalog/<int:pk>/', UsefulCatalogDetailAPIView.as_view()),

    path("get_months/", get_months, name="get-months"),
    path("get_days/<int:month>", get_days, name="get-days"),
    path("get_groups_products/<int:month>/<int:day>/", get_products_len_in_a_day_by_groups, name="get-groups-products"),
    path('webappbot/', IndexViewWebAppBot.as_view(), name='index'),
    path('example/', IndexViewExample.as_view(), name='example'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  