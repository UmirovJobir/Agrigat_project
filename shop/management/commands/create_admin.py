import os
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            email    = os.environ.get('ADMIN_EMAIL')
            username = os.environ.get('ADMIN_LOGIN')
            password = os.environ.get('ADMIN_PASSWORD')
            self.stdout.write('Creating account for %s %s' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            self.stdout.write(f"Created user '{admin}'")
        else:
            self.stdout.write('Admin accounts can only be initialized if no Accounts exist')


