import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()
from django.shortcuts import get_object_or_404
import pandas as pd
from shop.models import Category


file = 'cat_rel.xlsx'
# file = 'cat_07_02.xlsx'
# file = 'category.txt'
# csv_file = 'mini.csv'

df = pd.read_excel(file)

for i in df.values:
    print(i[0],i[1])
    # a = Category.objects.create(id=i[0], name=i[1])
    a = get_object_or_404(Category, id=i[1])
    a.parent = get_object_or_404(Category, id=i[0])
    a.save()
    print(a)
