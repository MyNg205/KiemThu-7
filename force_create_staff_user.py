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
