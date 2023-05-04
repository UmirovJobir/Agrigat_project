from django.core.management import BaseCommand
from shop.models import Product, Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        groups = Group.objects.all()

        product_count = 0

        for product in products:
            for group in groups:
                if product.group_id == group.group_id:
                    product.group_test = group
                    product.save()
                    product_count += 1
        self.stdout.write(f"updated {product_count} query.")

# timestep_to_datatime(1679737503)
