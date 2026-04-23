from _script_setup import setup

setup()

from django.contrib.auth.models import User

from hotel.models import UserProfile


def create_staff_account():
    username = "staff1"
    password = "staff12345"
    email = "staff1@sandyhotel.vn"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": "Staff",
            "is_staff": True,
            "is_active": True,
        },
    )

    user.email = email
    user.first_name = "Staff"
    user.is_staff = True
    user.is_active = True
    user.set_password(password)
    user.save()

    UserProfile.objects.get_or_create(user=user)

    action = "Created" if created else "Updated"
    print(f"{action} staff account: {username} / {password}")


if __name__ == "__main__":
    create_staff_account()
