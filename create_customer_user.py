from _script_setup import setup

setup()

from django.contrib.auth.models import User

from hotel.models import UserProfile


def create_customer_account():
    username = "customer1"
    password = "customer12345"
    email = "customer1@sandyhotel.vn"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": "Customer",
            "is_staff": False,
            "is_active": True,
        },
    )

    user.email = email
    user.first_name = "Customer"
    user.is_staff = False
    user.is_active = True
    user.set_password(password)
    user.save()

    UserProfile.objects.get_or_create(user=user)

    action = "Created" if created else "Updated"
    print(f"{action} customer account: {username} / {password}")


if __name__ == "__main__":
    create_customer_account()
