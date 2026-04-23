#!/usr/bin/env python
"""
Test script để kiểm tra đăng nhập
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from django.contrib.auth.models import User
from hotel.models import UserProfile

print("\n" + "="*60)
print("✅ THÔNG TIN ĐĂNG NHẬP - CHÍNH XÁC")
print("="*60)

print("\n📋 NHÂN VIÊN (STAFF):")
print("   Email: staff@hotel.com")
print("   Password: staff123")
print("   Quyền: is_staff = True")

print("\n👤 KHÁCH HÀNG (CUSTOMER):")
print("   Email: customer@hotel.com")
print("   Password: customer123")
print("   Quyền: is_staff = False")

print("\n" + "="*60)
print("🌐 TRUY CẬP: http://localhost:8000/login/")
print("="*60 + "\n")

# Kiểm tra users trong DB
print("📊 KIỂM TRA DỮ LIỆU TRONG DATABASE:\n")
for user in User.objects.all():
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Is Staff: {user.is_staff}")
    print(f"  Is Active: {user.is_active}")
    print()

