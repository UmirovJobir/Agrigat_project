from django.core.management import BaseCommand
from datetime import datetime
import pytz

from shop.models import Product


def timestep_to_datatime(timestep):
    local_tz = pytz.timezone("Asia/Tashkent") 
    utc_dt = datetime.utcfromtimestamp(timestep).replace(tzinfo=pytz.utc)
    local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))
    
    return local_dt

class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        product_count = 0
        for product in products:
            product.datetime = timestep_to_datatime(product.timestep)
            product.save()
            product_count += 1

        self.stdout.write(f"{product_count}")


