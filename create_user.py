from _script_setup import setup

setup()

from django.contrib.auth.models import User


def recreate_admin_user():
    User.objects.filter(username="admin").delete()

    user = User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="pass12345",
        first_name="Admin",
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )

    print("Created admin user")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print("Password: pass12345")


if __name__ == "__main__":
    recreate_admin_user()
