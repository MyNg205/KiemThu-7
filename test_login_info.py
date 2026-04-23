#!/usr/bin/env python
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KIEMTHU.settings")
django.setup()

from django.contrib.auth.models import User


def main():
    print("\n" + "=" * 60)
    print("LOGIN INFO")
    print("=" * 60)

    print("\nSTAFF:")
    print("  Email: staff@hotel.com")
    print("  Password: staff123")
    print("  Role: is_staff = True")

    print("\nCUSTOMER:")
    print("  Email: customer@hotel.com")
    print("  Password: customer123")
    print("  Role: is_staff = False")

    print("\n" + "=" * 60)
    print("LOGIN URL: http://localhost:8000/login/")
    print("=" * 60 + "\n")

    print("DATABASE USERS:\n")
    for user in User.objects.all():
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Is Active: {user.is_active}")
        print()


if __name__ == "__main__":
    main()
