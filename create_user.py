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

