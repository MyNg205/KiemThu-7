from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class RegisterViewTests(TestCase):
    def test_customer_can_register_account(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Nguyen Van A',
                'email': 'customer@example.com',
                'phone': '0912345678',
                'age': 25,
                'password': 'secret123',
                'confirm_password': 'secret123',
            },
        )

        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(email='customer@example.com')
        profile = UserProfile.objects.get(user=user)

        self.assertEqual(user.username, 'customer@example.com')
        self.assertEqual(user.first_name, 'Nguyen Van A')
        self.assertFalse(user.is_staff)
        self.assertEqual(profile.phone, '0912345678')
        self.assertEqual(profile.age, 25)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(
            username='customer@example.com',
            email='customer@example.com',
            password='secret123',
        )

        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Nguoi Moi',
                'email': 'customer@example.com',
                'phone': '0988888888',
                'age': 20,
                'password': 'secret123',
                'confirm_password': 'secret123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email đã được sử dụng.')
        self.assertEqual(User.objects.filter(email='customer@example.com').count(), 1)

    def test_register_rejects_invalid_phone_number(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Nguyen Van A',
                'email': 'customer2@example.com',
                'phone': '09abc12345',
                'age': 25,
                'password': 'secret123',
                'confirm_password': 'secret123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.')
        self.assertFalse(User.objects.filter(email='customer2@example.com').exists())

    def test_register_rejects_underage_customer(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Nguyen Van A',
                'email': 'customer3@example.com',
                'phone': '0912345678',
                'age': 16,
                'password': 'secret123',
                'confirm_password': 'secret123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tuổi phải từ 18 trở lên.')
        self.assertFalse(User.objects.filter(email='customer3@example.com').exists())

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Nguyen Van A',
                'email': 'customer4@example.com',
                'phone': '0912345678',
                'age': 25,
                'password': 'abcdefgh',
                'confirm_password': 'abcdefgh',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mật khẩu phải có ít nhất 1 chữ cái và 1 chữ số.')
        self.assertFalse(User.objects.filter(email='customer4@example.com').exists())
