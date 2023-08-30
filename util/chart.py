from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.contrib.admin.views.decorators import staff_member_required
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import JsonResponse
from shop.models import Product, TelegramGroupChannel, BotUser
import json


# @staff_member_required
# def get_years(request):
#     products_years = Product.objects.annotate(year=ExtractYear("datetime")).values("year").order_by("-year").distinct()
#     years = [product["year"] for product in products_years]

#     return JsonResponse({
#         "options": years,
#     })


@staff_member_required
def get_months(request):
    products = Product.objects.annotate(month=ExtractMonth("datetime")).values("month").order_by("month").distinct()
    months = [product["month"] for product in products]
    
    return JsonResponse({
        "months": months,
        },)

@staff_member_required
def get_days(request, month):
    products = Product.objects.filter(datetime__month=month)
    days_group = products.annotate(day=ExtractDay("datetime")).values("day").order_by("day").distinct()
    days = [product["day"] for product in days_group]

    return JsonResponse({
        "days": days,
    })
    

@staff_member_required
def get_products_len_in_a_day_by_groups(request, month, day):
    products = Product.objects.filter(datetime__month=month, datetime__day=day)
    groups = TelegramGroupChannel.objects.filter(group__in=products).distinct()

    data = {}
    for group in groups:
        groups_products = products.filter(group=group)
        
        data[group.group_name]=len(groups_products)
        
    return JsonResponse({
        "groups": list(data.keys()),
        "products": list(data.values())
    })


