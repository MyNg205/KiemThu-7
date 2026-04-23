#!/usr/bin/env python
"""Wrapper to run Django commands from the hotel app directory."""
from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parent.parent


def main():
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KIEMTHU.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line([str(ROOT_DIR / "manage.py"), *sys.argv[1:]])


if __name__ == "__main__":
    main()
