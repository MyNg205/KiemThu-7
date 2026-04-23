<<<<<<< HEAD
from _script_setup import setup

setup()

from django.contrib.auth.models import User

from hotel.models import UserProfile


def upsert_user(username, email, password, is_staff, first_name, profile_defaults):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": first_name,
            "is_staff": is_staff,
            "is_active": True,
        },
    )

    user.email = email
    user.first_name = first_name
    user.is_staff = is_staff
    user.is_active = True
    user.set_password(password)
    user.save()

    UserProfile.objects.update_or_create(user=user, defaults=profile_defaults)
    action = "Created" if created else "Updated"
    print(f"{action} user: {username} ({email})")


if __name__ == "__main__":
    upsert_user(
        username="staff",
        email="staff@hotel.com",
        password="staff123",
        is_staff=True,
        first_name="Staff",
        profile_defaults={"phone": "0901234567", "age": 30},
    )
    upsert_user(
        username="customer",
        email="customer@hotel.com",
        password="customer123",
        is_staff=False,
        first_name="Customer",
        profile_defaults={"phone": "0987654321", "age": 25},
    )

    print("\nLogin credentials")
    print("Staff: staff@hotel.com / staff123")
    print("Customer: customer@hotel.com / customer123")
=======
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from django.contrib.auth.models import User
from hotel.models import UserProfile

# Tạo hoặc lấy tài khoản staff
staff_user, created = User.objects.get_or_create(
    username='staff',
    defaults={
        'email': 'staff@hotel.com',
        'first_name': 'Nhân Viên',
        'is_staff': True
    }
)
if created:
    staff_user.set_password('staff123')
    staff_user.save()
    status = "Tạo"
else:
    # Update password nếu user đã tồn tại
    staff_user.set_password('staff123')
    staff_user.is_staff = True
    staff_user.save()
    status = "Cập nhật"
UserProfile.objects.get_or_create(user=staff_user, defaults={'phone': '0901234567', 'age': 30})
print(f"✅ {status} tài khoản staff: {staff_user.username} (Email: {staff_user.email})")

# Tạo hoặc lấy tài khoản customer
customer_user, created = User.objects.get_or_create(
    username='customer',
    defaults={
        'email': 'customer@hotel.com',
        'first_name': 'Nguyễn Khách Hàng'
    }
)
if created:
    customer_user.set_password('customer123')
    customer_user.save()
    status = "Tạo"
else:
    customer_user.set_password('customer123')
    customer_user.is_staff = False
    customer_user.save()
    status = "Cập nhật"
UserProfile.objects.get_or_create(user=customer_user, defaults={'phone': '0987654321', 'age': 25})
print(f"✅ {status} tài khoản customer: {customer_user.username} (Email: {customer_user.email})")

print("\n=== THÔNG TIN ĐĂNG NHẬP ===")
print("📋 Staff Account:")
print(f"   Email: staff@hotel.com")
print(f"   Password: staff123")
print("\n👤 Customer Account:")
print(f"   Email: customer@hotel.com")
print(f"   Password: customer123")


>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
