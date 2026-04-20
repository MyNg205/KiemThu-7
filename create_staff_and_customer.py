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


