#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from django.contrib.auth.models import User
from hotel.models import UserProfile

print("=== DANH SÁCH USER HIỆN TẠI ===")
for user in User.objects.all():
    print(f"Username: {user.username}, Email: {user.email}, Is Staff: {user.is_staff}")

print("\n=== SỬA LỖI EMAIL ===")
# Sửa email cho staff
staff = User.objects.get(username='staff')
staff.email = 'staff@hotel.com'
staff.is_staff = True
staff.set_password('staff123')
staff.save()
print(f"✅ Cập nhật staff: Email={staff.email}, Password=staff123")

# Sửa email cho customer
customer = User.objects.get(username='customer')
customer.email = 'customer@hotel.com'
customer.is_staff = False
customer.set_password('customer123')
customer.save()
print(f"✅ Cập nhật customer: Email={customer.email}, Password=customer123")

print("\n=== THÔNG TIN ĐĂNG NHẬP CHÍNH XÁC ===")
print("📋 Tài khoản Nhân Viên (Staff):")
print(f"   Email: staff@hotel.com")
print(f"   Password: staff123")
print(f"   Is Staff: {staff.is_staff}")
print("\n👤 Tài khoản Khách Hàng (Customer):")
print(f"   Email: customer@hotel.com")
print(f"   Password: customer123")
print(f"   Is Staff: {customer.is_staff}")

