from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import JsonResponse
from shop.models import Product, Group, User
from shop.serializers import GroupSerializer
from django.db.models import Count, F, Sum, Avg
from datetime import datetime
import pandas as pd
import pytz
import json
from urllib.parse import urlencode

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]

def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    
    return year_dict



# @staff_member_required
# def get_years(request):
#     products_years = Product.objects.annotate(year=ExtractYear("datetime")).values("year").order_by("-year").distinct()
#     years = [product["year"] for product in products_years]

#     return JsonResponse({
#         "options": years,
#     })


def get_groups(request):
    groups = Group.objects.all()
    group_ids = [group.id for group in groups]

    return JsonResponse({
        "months": group_ids,
    })


def get_months(request):
    products = Product.objects.annotate(month=ExtractMonth("datetime")).values("month").order_by("month").distinct()
    months = [product["month"] for product in products]
    
    return JsonResponse({
        "months": months,
        },)


def get_days(request, month):
    products = Product.objects.filter(datetime__month=month)
    days_group = products.annotate(day=ExtractDay("datetime")).values("day").order_by("day").distinct()
    days = [product["day"] for product in days_group]

    return JsonResponse({
        "days": days,
    })
    

def get_all_products_in_a_day(request, month, day):
    products = Product.objects.filter(datetime__month=month, datetime__day=day).distinct()
    product_ids = [f"{product.id}    {product.datetime}" for product in products]

    return JsonResponse({
        'len':len(product_ids),
        "product_id": product_ids,
    })

def get_products_len_in_a_day_by_groups(request, month, day):
    products = Product.objects.filter(datetime__month=month, datetime__day=day)
    groups = Group.objects.filter(group_test__in=products).distinct()

    data = {}
    for group in groups:
        groups_products = products.filter(group_test=group)
        
        data[group.group_name]=len(groups_products)
        
    return JsonResponse({
        "groups": list(data.keys()),
        "products": list(data.values())
    })







def home(request):
    users = User.objects.all()
    user_names = [user.user_name for user in users]
    user_ids = [user.user_id for user in users]

    config = {
        "type": "bar",
        "data": {
            "labels": user_names,
            "datasets": [{
                "label": "Foo",
                "data": user_ids
            }]
        }
    }

    params = {
        'chart': json.dumps(config),
        'width': 500,
        'height': 300,
        'backgroundColor': 'white',
    }
    print('https://quickchart.io/chart?%s' % urlencode(params))

    my_dict = {
        'link':'https://quickchart.io/chart?%s' % urlencode(params),
    }

    return render(request, 'admin/test_chart.html',context=my_dict)