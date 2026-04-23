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
