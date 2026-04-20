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

