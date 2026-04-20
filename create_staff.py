import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()

from django.contrib.auth.models import User, Group
from hotel.models import UserProfile

def create_staff_account():
    username = 'staff1'
    password = 'staff12345'
    email = 'staff1@sandyhotel.vn'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password, email=email, is_staff=True)
        user.first_name = 'Nhân viên'
        user.save()
        UserProfile.objects.get_or_create(user=user)
        print('Created staff account:', username, password)
    else:
        print('Staff account already exists')

if __name__ == '__main__':
    create_staff_account()
