<<<<<<< HEAD
from _script_setup import setup

setup()

from django.contrib.auth.models import User


def recreate_admin_user():
    User.objects.filter(username="admin").delete()

    user = User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="pass12345",
        first_name="Admin",
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )

    print("Created admin user")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print("Password: pass12345")


if __name__ == "__main__":
    recreate_admin_user()
=======
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from django.contrib.auth.models import User

# Xóa user cũ nếu tồn tại
User.objects.filter(username='admin').delete()

# Tạo user mới
user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='pass12345',
    first_name='Admin',
    is_staff=True,
    is_superuser=True
)

print(f"✅ User created successfully!")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Password: pass12345")

>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
