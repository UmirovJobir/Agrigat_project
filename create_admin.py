import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()
from agrozamin_hr.models.user_admin import User_admin
from django.conf import settings

def handle(*args, **options):
        if User_admin.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'hr-parol'
                print('Creating account for %s (%s)' % (username, email))
                admin = User_admin.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')

if __name__=='__main__':
    handle()