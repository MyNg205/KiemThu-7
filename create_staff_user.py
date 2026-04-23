from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    email = 'staff@sandyhotel.vn'
    password = '12345678'
    username = 'staff'
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_active=True
        )
        print(f"Tạo tài khoản nhân viên thành công: {email} / {password}")
    else:
        print(f"Tài khoản {email} đã tồn tại.")

