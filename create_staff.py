<<<<<<< HEAD
from _script_setup import setup

setup()

from django.contrib.auth.models import User

from hotel.models import UserProfile


def create_staff_account():
    username = "staff1"
    password = "staff12345"
    email = "staff1@sandyhotel.vn"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": "Staff",
            "is_staff": True,
            "is_active": True,
        },
    )

    user.email = email
    user.first_name = "Staff"
    user.is_staff = True
    user.is_active = True
    user.set_password(password)
    user.save()

    UserProfile.objects.get_or_create(user=user)

    action = "Created" if created else "Updated"
    print(f"{action} staff account: {username} / {password}")


if __name__ == "__main__":
=======
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
>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
    create_staff_account()
