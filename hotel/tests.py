import json
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Booking, Room, RoomType, UserProfile


class RegisterViewTests(TestCase):
    def test_customer_can_register_account(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Nguyen Van A",
                "email": "customer@example.com",
                "phone": "0912345678",
                "age": 25,
                "password": "secret123",
                "confirm_password": "secret123",
            },
        )

        self.assertRedirects(response, reverse("home"))
        user = User.objects.get(email="customer@example.com")
        profile = UserProfile.objects.get(user=user)

        self.assertEqual(user.username, "customer@example.com")
        self.assertEqual(user.first_name, "Nguyen Van A")
        self.assertFalse(user.is_staff)
        self.assertEqual(profile.phone, "0912345678")
        self.assertEqual(profile.age, 25)
        self.assertFalse(profile.profile_completed)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="secret123",
        )

        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Nguoi Moi",
                "email": "customer@example.com",
                "phone": "0988888888",
                "age": 20,
                "password": "secret123",
                "confirm_password": "secret123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email đã được sử dụng.")
        self.assertEqual(User.objects.filter(email="customer@example.com").count(), 1)

    def test_register_rejects_invalid_phone_number(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Nguyen Van A",
                "email": "customer2@example.com",
                "phone": "09abc12345",
                "age": 25,
                "password": "secret123",
                "confirm_password": "secret123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.")
        self.assertFalse(User.objects.filter(email="customer2@example.com").exists())

    def test_register_rejects_underage_customer(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Nguyen Van A",
                "email": "customer3@example.com",
                "phone": "0912345678",
                "age": 16,
                "password": "secret123",
                "confirm_password": "secret123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tuổi phải từ 18 trở lên.")
        self.assertFalse(User.objects.filter(email="customer3@example.com").exists())

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Nguyen Van A",
                "email": "customer4@example.com",
                "phone": "0912345678",
                "age": 25,
                "password": "abcdefgh",
                "confirm_password": "abcdefgh",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mật khẩu phải có ít nhất 1 chữ cái và 1 chữ số.")
        self.assertFalse(User.objects.filter(email="customer4@example.com").exists())


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="secret123",
            first_name="Nguyen Van A",
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone="0912345678",
            age=25,
            profile_completed=False,
        )
        self.client.login(username="customer@example.com", password="secret123")

    def test_new_customer_sees_welcome_profile_form(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "customer@example.com")
        self.assertContains(response, "Lưu thông tin")

    def test_profile_completion_marks_profile_completed(self):
        response = self.client.post(
            reverse("profile"),
            {
                "action": "complete",
                "full_name": "Nguyen Van B",
                "age": 30,
                "phone": "0987654321",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, "Nguyen Van B")
        self.assertEqual(self.profile.age, 30)
        self.assertEqual(self.profile.phone, "0987654321")
        self.assertTrue(self.profile.profile_completed)

    def test_profile_update_rejects_underage_customer(self):
        self.profile.profile_completed = True
        self.profile.save()

        response = self.client.post(
            reverse("profile"),
            {
                "action": "update",
                "full_name": "Nguyen Van A",
                "age": 17,
                "phone": "0912345678",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tuổi phải từ 18 trở lên.")

    def test_customer_label_switches_to_loyal_after_more_than_three_bookings(self):
        self.profile.profile_completed = True
        self.profile.save()
        room_type = RoomType.objects.create(
            name="Studio",
            description="Test",
            base_price=1000000,
            capacity=2,
            bed_count=1,
        )
        room = Room.objects.create(room_type=room_type, room_number="101", floor=1, status="available")
        for index in range(4):
            Booking.objects.create(
                user=self.user,
                room=room,
                check_in=f"2026-05-0{index + 1}",
                check_out=f"2026-05-1{index + 1}",
                status="Đã đặt",
            )

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Khách hàng thân thiết")
        self.assertContains(response, "Cập nhật thông tin")


class BookRoomViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="secret123",
            first_name="Thanh Minh",
        )
        self.profile = UserProfile.objects.create(user=self.user, phone="0398814925", age=30, profile_completed=True)
        self.client.login(username="customer@example.com", password="secret123")

        self.studio = RoomType.objects.create(
            name="Studio",
            description="Phòng Studio",
            base_price=1050000,
            capacity=2,
            bed_count=1,
            amenities="WiFi,TV,Minibar",
        )
        self.deluxe = RoomType.objects.create(
            name="Deluxe",
            description="Phòng Deluxe",
            base_price=1700000,
            capacity=3,
            bed_count=1,
            amenities="WiFi,TV,AC,Minibar",
        )
        self.studio_room_1 = Room.objects.create(room_type=self.studio, room_number="101", floor=1, status="available")
        self.studio_room_2 = Room.objects.create(room_type=self.studio, room_number="102", floor=1, status="available")
        self.deluxe_room_1 = Room.objects.create(room_type=self.deluxe, room_number="201", floor=2, status="available")
        self.deluxe_room_2 = Room.objects.create(room_type=self.deluxe, room_number="202", floor=2, status="available")

    def test_search_then_select_room_type_shows_confirmation_form(self):
        check_in = (date.today() + timedelta(days=2)).isoformat()
        check_out = (date.today() + timedelta(days=5)).isoformat()

        response = self.client.get(
            reverse("book_room"),
            {
                "check_in": check_in,
                "check_out": check_out,
                "room_type": self.deluxe.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thông tin cá nhân")
        self.assertContains(response, "Phòng đã chọn")
        self.assertContains(response, "Đặt thêm phòng khác")

    def test_post_booking_can_create_multiple_rooms_in_one_request(self):
        check_in = (date.today() + timedelta(days=2)).isoformat()
        check_out = (date.today() + timedelta(days=5)).isoformat()

        response = self.client.post(
            reverse("book_room"),
            {
                "check_in": check_in,
                "check_out": check_out,
                "selected_rooms_data": json.dumps(
                    [
                        {"room_type_id": self.deluxe.id, "quantity": 1},
                        {"room_type_id": self.studio.id, "quantity": 1},
                    ]
                ),
                "name": "Thanh Minh",
                "age": "30",
                "phone": "0398814925",
                "guest_count": "4",
                "special_request": "Them goi cao hon",
            },
        )

        self.assertRedirects(response, reverse("booking_history"))
        bookings = Booking.objects.filter(user=self.user).order_by("room__room_number")

        self.assertEqual(bookings.count(), 2)
        self.assertEqual(bookings[0].guest_count, 4)
        self.assertEqual(bookings[0].special_request, "Them goi cao hon")
        self.assertEqual(bookings[0].booking_group, bookings[1].booking_group)

    def test_post_booking_rejects_guest_count_exceeding_capacity(self):
        check_in = (date.today() + timedelta(days=2)).isoformat()
        check_out = (date.today() + timedelta(days=5)).isoformat()

        response = self.client.post(
            reverse("book_room"),
            {
                "check_in": check_in,
                "check_out": check_out,
                "selected_rooms_data": json.dumps([{"room_type_id": self.studio.id, "quantity": 1}]),
                "name": "Thanh Minh",
                "age": "30",
                "phone": "0398814925",
                "guest_count": "5",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Số khách vượt quá sức chứa của các phòng đã chọn.")
        self.assertEqual(Booking.objects.count(), 0)


class RoomTypeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer@example.com",
            email="viewer@example.com",
            password="secret123",
        )
        self.client.login(username="viewer@example.com", password="secret123")
        self.studio = RoomType.objects.create(
            name="Studio",
            description="Phòng Studio",
            base_price=1050000,
            capacity=2,
            bed_count=1,
            amenities="WiFi,TV,Minibar",
        )
        self.suite = RoomType.objects.create(
            name="Suite",
            description="Phòng Suite",
            base_price=2800000,
            capacity=4,
            bed_count=1,
            amenities="WiFi,TV,AC,Minibar",
        )

    def test_room_type_detail_shows_type_specific_content(self):
        response = self.client.get(reverse("room_type_detail", args=[self.suite.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Suite")
        self.assertContains(response, "55 m2")
        self.assertContains(response, "Set trái cây chào mừng")
        self.assertContains(response, "Đặt phòng ngay")

    def test_room_type_detail_uses_different_copy_for_other_type(self):
        response = self.client.get(reverse("room_type_detail", args=[self.studio.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "28 m2")
        self.assertContains(response, "Khu bếp nhỏ gọn")
