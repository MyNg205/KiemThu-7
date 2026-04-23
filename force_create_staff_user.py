<<<<<<< HEAD
from _script_setup import setup

setup()

from django.contrib.auth.models import User

from hotel.models import UserProfile


def recreate_staff_user():
    email = "staff@sandyhotel.vn"
    password = "12345678"
    username = "staff"

    User.objects.filter(email=email).delete()
    User.objects.filter(username=username).delete()

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name="Staff",
        is_staff=True,
        is_active=True,
    )
    UserProfile.objects.get_or_create(user=user)
    print(f"Created staff account: {email} / {password}")


if __name__ == "__main__":
    recreate_staff_user()
=======
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()
from django.contrib.auth.models import User

email = 'staff@sandyhotel.vn'
password = '12345678'
username = 'staff'

# Xóa user cũ nếu tồn tại (theo email hoặc username)
User.objects.filter(email=email).delete()
User.objects.filter(username=username).delete()

user = User.objects.create_user(
    username=username,
    email=email,
    password=password,
    is_staff=True,
    is_active=True
)
print(f"Tạo tài khoản nhân viên thành công: {email} / {password}")

>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
