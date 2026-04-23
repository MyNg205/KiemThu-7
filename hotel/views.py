import json
import re
from datetime import date
from uuid import uuid4

from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Booking, Room, RoomType, UserProfile


CANCELLED_STATUS = "Đã huỷ"
BOOKED_STATUS = "Đã đặt"
CHECKED_IN_STATUS = "Đã check in"

ROOM_IMAGE_MAP = {
    "studio": "images/studio.jpg",
    "deluxe": "images/deluxe.png",
    "family": "images/family.jpg",
    "suite": "images/suite.jpg",
}


ROOM_DESCRIPTION_MAP = {
    "studio": "Phòng Studio hiện đại, nội thất ấm áp và bố cục gọn gàng, phù hợp cho cặp đôi hoặc khách công tác nghỉ dưỡng ngắn ngày.",
    "deluxe": "Phòng Deluxe rộng rãi, có ban công đón sáng và cảm giác thư thái, phù hợp cho kỳ nghỉ sang trọng nhưng vẫn ấm cúng.",
    "family": "Phòng Family thoáng rộng cho gia đình hoặc nhóm bạn, bố trí linh hoạt để nghỉ dưỡng thoải mái trong nhiều ngày.",
    "suite": "Phòng Suite cao cấp với không gian tiếp khách riêng, tầm nhìn đẹp và trải nghiệm nghỉ dưỡng chỉn chu hơn.",
}


ROOM_DETAIL_MAP = {
    "studio": {
        "headline": "Gọn gàng, sáng sủa và vừa đủ cho một kỳ nghỉ thư thả.",
        "short_description": "Studio phù hợp cho khách đi công tác hoặc cặp đôi cần không gian riêng tư, tiện nghi và dễ chịu ngay trung tâm nghỉ dưỡng.",
        "room_size": "28 m2",
        "view": "View phố và khoảng sân xanh nội khu",
        "services": [
            "Dọn phòng mỗi ngày",
            "Nước suối, trà và cà phê miễn phí",
            "Hỗ trợ lễ tân 24/7",
        ],
        "amenities": [
            "Giường cỡ lớn êm ái",
            "Khu bếp nhỏ gọn",
            "Máy lạnh và TV thông minh",
            "WiFi tốc độ cao",
            "Phòng tắm riêng với vòi sen",
            "Bàn làm việc tiện lợi",
        ],
        "rules": [
            "Không hút thuốc trong phòng",
            "Nhận phòng từ 14:00, trả phòng trước 12:00",
            "Phù hợp tối đa 2 người lớn",
        ],
        "gallery": [
            {"image": "images/studio.jpg", "title": "Không gian ngủ", "position": "center center"},
            {"image": "images/studio.jpg", "title": "Góc tiếp khách nhỏ", "position": "center 35%"},
            {"image": "images/studio.jpg", "title": "Khu bếp và cửa sổ", "position": "center 65%"},
        ],
    },
    "deluxe": {
        "headline": "Rộng hơn, sang hơn và rất hợp cho một kỳ nghỉ ngắn ngày đầy đủ tiện nghi.",
        "short_description": "Deluxe mang lại cảm giác cân bằng giữa sự thư giãn và tính riêng tư, thích hợp cho khách muốn ở thoải mái hơn với không gian mở và ánh sáng tự nhiên.",
        "room_size": "36 m2",
        "view": "View ban công đón nắng và thành phố",
        "services": [
            "Dọn phòng mỗi ngày",
            "Set minibar cơ bản",
            "Hỗ trợ giữ hành lý trước và sau giờ lưu trú",
        ],
        "amenities": [
            "Giường cỡ lớn cao cấp",
            "Ban công riêng",
            "TV thông minh và truyền hình cáp",
            "Máy sấy tóc, bàn ủi theo yêu cầu",
            "WiFi tốc độ cao",
            "Két an toàn cá nhân",
        ],
        "rules": [
            "Không hút thuốc trong phòng",
            "Không mang vật nuôi vào khu lưu trú",
            "Phù hợp tối đa 3 người lớn",
        ],
        "gallery": [
            {"image": "images/deluxe.png", "title": "Toàn cảnh phòng", "position": "center center"},
            {"image": "images/deluxe.png", "title": "Giường và nội thất", "position": "center 38%"},
            {"image": "images/deluxe.png", "title": "Góc ban công", "position": "center 68%"},
        ],
    },
    "family": {
        "headline": "Thoải mái cho cả gia đình với bố trí linh hoạt và cảm giác ấm cúng.",
        "short_description": "Family là lựa chọn phù hợp cho nhóm bạn hoặc gia đình nhỏ cần không gian lưu trú rộng rãi, thuận tiện sinh hoạt và nghỉ ngơi cùng nhau.",
        "room_size": "45 m2",
        "view": "View hồ bơi và khuôn viên khách sạn",
        "services": [
            "Dọn phòng mỗi ngày",
            "Bổ sung khăn, gối phụ theo yêu cầu",
            "Ưu tiên hỗ trợ gia đình có trẻ nhỏ",
        ],
        "amenities": [
            "Nhiều khu vực ngủ linh hoạt",
            "Bàn ăn nhỏ trong phòng",
            "TV thông minh",
            "Tủ lạnh và minibar",
            "Máy lạnh công suất lớn",
            "Phòng tắm rộng rãi",
        ],
        "rules": [
            "Không hút thuốc trong phòng",
            "Giữ yên tĩnh sau 22:00",
            "Phù hợp tối đa 4 người lớn",
        ],
        "gallery": [
            {"image": "images/family.jpg", "title": "Không gian chung", "position": "center center"},
            {"image": "images/family.jpg", "title": "Khu giường ngủ", "position": "center 35%"},
            {"image": "images/family.jpg", "title": "Góc sinh hoạt", "position": "center 70%"},
        ],
    },
    "suite": {
        "headline": "Hạng phòng cao cấp nhất với không gian riêng tư và trải nghiệm nghỉ dưỡng chỉn chu.",
        "short_description": "Suite phù hợp cho khách cần cảm giác sang trọng hơn, có khu tiếp khách riêng và không gian thư giãn rõ ràng cho kỳ nghỉ đặc biệt.",
        "room_size": "55 m2",
        "view": "View toàn cảnh thành phố và khoảng xanh ven biển",
        "services": [
            "Dọn phòng mỗi ngày",
            "Set trái cây chào mừng",
            "Ưu tiên hỗ trợ check-in sớm theo tình trạng phòng",
        ],
        "amenities": [
            "Phòng ngủ và khu tiếp khách tách biệt",
            "Giường cỡ lớn cao cấp",
            "TV thông minh ở nhiều khu vực",
            "Máy pha cà phê và minibar",
            "Phòng tắm rộng với tiện nghi đầy đủ",
            "WiFi tốc độ cao và bàn làm việc lớn",
        ],
        "rules": [
            "Không hút thuốc trong phòng",
            "Không tổ chức tiệc trong phòng",
            "Phù hợp tối đa 4 người lớn",
        ],
        "gallery": [
            {"image": "images/suite-gallery-2.png", "title": "Không gian ngủ suite", "position": "center center"},
            {"image": "images/suite-gallery-1.webp", "title": "Góc nội thất và bàn làm việc", "position": "center center"},
            {"image": "images/suite-gallery-3.webp", "title": "Khu nghỉ ngơi riêng tư", "position": "center center"},
        ],
    },
}


def build_room_type_cards(room_types):
    cards = []
    for room_type in room_types:
        cards.append(
            {
                "id": room_type.id,
                "name": room_type.name,
                "description": ROOM_DESCRIPTION_MAP.get(room_type.name.lower(), room_type.description),
                "base_price": room_type.base_price,
                "capacity": room_type.capacity,
                "bed_count": room_type.bed_count,
                "image": room_type.image,
                "local_image": ROOM_IMAGE_MAP.get(room_type.name.lower()),
                "available_count": getattr(room_type, "available_count", 0),
                "amenities": [item.strip() for item in room_type.amenities.split(",") if item.strip()][:4],
            }
        )
    return cards


def get_available_rooms(check_in, check_out):
    conflicting_room_ids = Booking.objects.exclude(status=CANCELLED_STATUS).filter(
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).values_list("room_id", flat=True)
    return (
        Room.objects.filter(status="available")
        .exclude(id__in=conflicting_room_ids)
        .select_related("room_type")
        .order_by("room_type__base_price", "floor", "room_number")
    )


def parse_date_range(check_in_value, check_out_value):
    if not check_in_value or not check_out_value:
        return None, None, ""

    try:
        check_in = date.fromisoformat(check_in_value)
        check_out = date.fromisoformat(check_out_value)
    except ValueError:
        return None, None, "Ngày lưu trú không hợp lệ."

    if check_out <= check_in:
        return None, None, "Ngày đi phải sau ngày đến."
    if check_in < date.today():
        return None, None, "Ngày đến không được nhỏ hơn ngày hiện tại."
    return check_in, check_out, ""


def parse_selected_rooms_payload(raw_payload):
    try:
        payload = json.loads(raw_payload or "[]")
    except json.JSONDecodeError:
        return []

    selected_items = []
    for item in payload:
        room_type_id = str(item.get("room_type_id", "")).strip()
        try:
            quantity = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0
        if room_type_id and quantity > 0:
            selected_items.append({"room_type_id": room_type_id, "quantity": quantity})
    return selected_items


def build_selected_room_cards(selected_items, room_cards, night_count):
    card_map = {str(card["id"]): card for card in room_cards}
    selected_cards = []

    for item in selected_items:
        room_card = card_map.get(str(item["room_type_id"]))
        if not room_card:
            continue
        quantity = min(item["quantity"], room_card["available_count"])
        if quantity <= 0:
            continue
        line_total = room_card["base_price"] * quantity * night_count
        selected_cards.append(
            {
                **room_card,
                "room_type_id": room_card["id"],
                "quantity": quantity,
                "line_total": line_total,
            }
        )
    return selected_cards


def calculate_selected_totals(selected_room_cards, guest_count):
    total_rooms = sum(item["quantity"] for item in selected_room_cards)
    total_capacity = sum(item["capacity"] * item["quantity"] for item in selected_room_cards)
    total_cost = sum(item["line_total"] for item in selected_room_cards)
    max_guest_count = max(total_capacity, 1)
    return {
        "total_rooms": total_rooms,
        "total_capacity": total_capacity,
        "total_cost": total_cost,
        "max_guest_count": max_guest_count,
    }


@login_required(login_url="/login/")
def home(request):
    if request.user.is_staff:
        return redirect("staff_home")

    room_types = RoomType.objects.annotate(
        available_count=Count("rooms", filter=Q(rooms__status="available"))
    )
    room_cards = build_room_type_cards(room_types)

    context = {
        "room_types": room_cards,
        "featured_room": room_cards[0] if room_cards else None,
        "secondary_room": room_cards[1] if len(room_cards) > 1 else (room_cards[0] if room_cards else None),
        "available_room_total": Room.objects.filter(status="available").count(),
    }
    return render(request, "home_customer.html", context)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        min_length=2,
        error_messages={
            "required": "Vui lòng nhập họ tên.",
            "min_length": "Họ tên phải có ít nhất 2 ký tự.",
            "max_length": "Họ tên không được vượt quá 150 ký tự.",
        },
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={
            "required": "Vui lòng nhập email.",
            "invalid": "Email không đúng định dạng.",
        },
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        error_messages={
            "required": "Vui lòng nhập số điện thoại.",
            "min_length": "Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.",
            "max_length": "Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.",
        },
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        required=False,
        error_messages={
            "invalid": "Tuổi phải là số hợp lệ.",
            "min_value": "Tuổi phải từ 18 trở lên.",
            "max_value": "Tuổi không được vượt quá 100.",
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            "required": "Vui lòng nhập mật khẩu.",
            "min_length": "Mật khẩu phải có ít nhất 8 ký tự.",
        },
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            "required": "Vui lòng xác nhận mật khẩu.",
            "min_length": "Mật khẩu xác nhận phải có ít nhất 8 ký tự.",
        },
    )

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())
        if not full_name:
            raise forms.ValidationError("Vui lòng nhập họ tên.")
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError("Họ tên không được chứa chữ số.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email đã được sử dụng.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"0\d{9}", phone):
            raise forms.ValidationError(
                "Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ."
            )
        return phone

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise forms.ValidationError("Mật khẩu phải có ít nhất 1 chữ cái và 1 chữ số.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Mật khẩu xác nhận không khớp.")
        return cleaned_data


class ProfileForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        min_length=2,
        error_messages={
            "required": "Vui lòng nhập họ tên.",
            "min_length": "Họ tên phải có ít nhất 2 ký tự.",
            "max_length": "Họ tên không được vượt quá 150 ký tự.",
        },
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        error_messages={
            "required": "Vui lòng nhập tuổi.",
            "invalid": "Tuổi phải là số hợp lệ.",
            "min_value": "Tuổi phải từ 18 trở lên.",
            "max_value": "Tuổi không được vượt quá 100.",
        },
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        error_messages={
            "required": "Vui lòng nhập số điện thoại.",
            "min_length": "Số điện thoại phải gồm đúng 10 chữ số.",
            "max_length": "Số điện thoại phải gồm đúng 10 chữ số.",
        },
    )

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())
        if not full_name:
            raise forms.ValidationError("Vui lòng nhập họ tên.")
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError("Họ tên không được chứa chữ số.")
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"0\d{9}", phone):
            raise forms.ValidationError("Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")
        return phone


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect("home")
                return render(request, "login.html", {"form": form, "error": "Email hoặc mật khẩu không chính xác"})
            except User.DoesNotExist:
                return render(request, "login.html", {"form": form, "error": "Email hoặc mật khẩu không chính xác"})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            age = form.cleaned_data.get("age")
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=full_name,
                password=password,
            )
            UserProfile.objects.create(user=user, phone=phone, age=age, profile_completed=False)
            login(request, user)
            messages.success(request, "Đăng ký tài khoản thành công.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    booking_count = Booking.objects.filter(user=request.user).exclude(status=CANCELLED_STATUS).count()
    customer_label = "Khách hàng thân thiết" if booking_count > 3 else "Khách hàng mới"
    initials = "".join(part[0] for part in request.user.first_name.split()[:2]).upper() or request.user.email[:2].upper()
    is_edit_mode = request.GET.get("edit") == "1"

    initial_data = {
        "full_name": request.user.first_name,
        "age": profile.age,
        "phone": profile.phone,
    }

    if request.method == "POST":
        form = ProfileForm(request.POST)
        action = request.POST.get("action", "save")
        if form.is_valid():
            request.user.first_name = form.cleaned_data["full_name"]
            request.user.save()
            profile.age = form.cleaned_data["age"]
            profile.phone = form.cleaned_data["phone"]
            profile.profile_completed = True
            profile.save()
            messages.success(request, "Lưu thông tin thành công!")
            return redirect("profile")
        is_edit_mode = action == "update"
    else:
        form = ProfileForm(initial=initial_data)

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "profile_form": form,
            "customer_label": customer_label,
            "booking_count": booking_count,
            "initials": initials,
            "is_new_customer": not profile.profile_completed,
            "is_edit_mode": is_edit_mode and profile.profile_completed,
        },
    )


@login_required(login_url="/login/")
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "booking_history.html", {"bookings": bookings})


@login_required(login_url="/login/")
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "room_detail.html", {"room": room})


@login_required(login_url="/login/")
def book_room(request, room_id=None):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    today_iso = date.today().isoformat()

    search_check_in = request.GET.get("check_in", "").strip()
    search_check_out = request.GET.get("check_out", "").strip()
    selected_room_type_id = request.GET.get("room_type", "").strip()
    search_performed = bool(search_check_in and search_check_out)
    search_error = ""
    booking_error = ""
    room_cards = []
    selected_room_cards = []
    nights = 0
    guest_count = 2
    special_request = ""

    if request.method == "POST":
        search_check_in = request.POST.get("check_in", "").strip()
        search_check_out = request.POST.get("check_out", "").strip()
        raw_selected_rooms = request.POST.get("selected_rooms_data", "[]")
        selected_items = parse_selected_rooms_payload(raw_selected_rooms)
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        age = request.POST.get("age", "").strip()
        special_request = request.POST.get("special_request", "").strip()

        try:
            guest_count = int(request.POST.get("guest_count", 1))
        except (TypeError, ValueError):
            guest_count = 1

        check_in, check_out, search_error = parse_date_range(search_check_in, search_check_out)
        if not search_error:
            nights = (check_out - check_in).days
            available_rooms = get_available_rooms(check_in, check_out)
            available_room_types = (
                RoomType.objects.filter(rooms__in=available_rooms)
                .annotate(available_count=Count("rooms", filter=Q(rooms__in=available_rooms), distinct=True))
                .distinct()
                .order_by("base_price")
            )
            room_cards = build_room_type_cards(available_room_types)
            selected_room_cards = build_selected_room_cards(selected_items, room_cards, nights)
            totals = calculate_selected_totals(selected_room_cards, guest_count)

            if not selected_room_cards:
                booking_error = "Vui lòng chọn ít nhất một loại phòng để tiếp tục."
            elif not name:
                booking_error = "Vui lòng nhập họ tên."
            elif not re.fullmatch(r"0\d{9}", phone):
                booking_error = "Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0."
            else:
                try:
                    age_value = int(age)
                except (TypeError, ValueError):
                    age_value = 0

                if age_value < 18:
                    booking_error = "Khách đặt phòng phải từ 18 tuổi trở lên."
                elif guest_count > totals["total_capacity"]:
                    booking_error = "Số khách vượt quá sức chứa của các phòng đã chọn."
                else:
                    booking_group = uuid4().hex[:12].upper()
                    rooms_to_book = []

                    for item in selected_room_cards:
                        matched_rooms = list(
                            available_rooms.filter(room_type_id=item["room_type_id"]).order_by("room_number")[: item["quantity"]]
                        )
                        if len(matched_rooms) < item["quantity"]:
                            booking_error = f"Loại phòng {item['name']} không còn đủ số lượng trống."
                            break
                        rooms_to_book.extend(matched_rooms)

                    if not booking_error:
                        created_count = 0
                        for room in rooms_to_book:
                            Booking.objects.create(
                                user=user,
                                room=room,
                                check_in=check_in,
                                check_out=check_out,
                                guest_count=guest_count,
                                special_request=special_request,
                                booking_group=booking_group,
                                status=BOOKED_STATUS,
                            )
                            created_count += 1

                        user.first_name = name
                        user.save()
                        user_profile.phone = phone
                        user_profile.age = age_value
                        user_profile.profile_completed = True
                        user_profile.save()

                        messages.success(
                            request,
                            f"Đặt phòng thành công. Bạn đã giữ {created_count} phòng với mã nhóm {booking_group}.",
                        )
                        return redirect("booking_history")
        search_performed = bool(search_check_in and search_check_out)
    else:
        if search_performed:
            check_in, check_out, search_error = parse_date_range(search_check_in, search_check_out)
            if not search_error:
                nights = (check_out - check_in).days
                available_rooms = get_available_rooms(check_in, check_out)
                available_room_types = (
                    RoomType.objects.filter(rooms__in=available_rooms)
                    .annotate(available_count=Count("rooms", filter=Q(rooms__in=available_rooms), distinct=True))
                    .distinct()
                    .order_by("base_price")
                )
                room_cards = build_room_type_cards(available_room_types)

                if room_id:
                    selected_room = available_rooms.filter(id=room_id).first()
                    if selected_room:
                        selected_room_type_id = str(selected_room.room_type_id)

                if selected_room_type_id:
                    selected_room_cards = build_selected_room_cards(
                        [{"room_type_id": selected_room_type_id, "quantity": 1}],
                        room_cards,
                        nights,
                    )

        guest_count = min(2, calculate_selected_totals(selected_room_cards, 2)["max_guest_count"]) if selected_room_cards else 2

    totals = calculate_selected_totals(selected_room_cards, guest_count)
    selected_rooms_payload = json.dumps(
        [{"room_type_id": item["room_type_id"], "quantity": item["quantity"]} for item in selected_room_cards]
    )
    stay_check_in = None
    stay_check_out = None
    if selected_room_cards:
        try:
            stay_check_in = date.fromisoformat(search_check_in)
            stay_check_out = date.fromisoformat(search_check_out)
        except ValueError:
            stay_check_in = None
            stay_check_out = None

    template_name = "book_room_confirm.html" if selected_room_cards or request.method == "POST" else "book_room.html"

    return render(
        request,
        template_name,
        {
            "today_iso": today_iso,
            "search_check_in": search_check_in,
            "search_check_out": search_check_out,
            "search_performed": search_performed,
            "search_error": search_error,
            "booking_error": booking_error,
            "room_cards": room_cards,
            "selected_room_cards": selected_room_cards,
            "selected_rooms_payload": selected_rooms_payload,
            "selected_room_type_id": selected_room_type_id,
            "nights": nights,
            "stay_check_in": stay_check_in,
            "stay_check_out": stay_check_out,
            "guest_count": max(1, min(guest_count, totals["max_guest_count"])),
            "max_guest_count": totals["max_guest_count"],
            "total_room_count": totals["total_rooms"],
            "total_capacity": totals["total_capacity"],
            "total_cost": totals["total_cost"],
            "special_request": special_request,
            "form_name": user.first_name,
            "form_phone": user_profile.phone,
            "form_age": user_profile.age,
            "form_email": user.email,
        },
    )


@login_required(login_url="/login/")
def select_room_to_book(request):
    room_types = RoomType.objects.all()
    if request.method == "POST":
        room_type_id = request.POST.get("room_type_id")
        if room_type_id:
            return redirect("room_detail", room_id=room_type_id)
    return render(request, "select_room_to_book.html", {"room_types": room_types})


@login_required(login_url="/login/")
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        booking.status = CANCELLED_STATUS
        booking.save()
        booking.room.status = "available"
        booking.room.save()
        messages.success(request, "Đã huỷ đặt phòng thành công.")
        return redirect("booking_history")
    return render(request, "cancel_booking.html", {"booking": booking})


@login_required(login_url="/login/")
def room_type_detail(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    room_key = room_type.name.lower()
    detail = ROOM_DETAIL_MAP.get(
        room_key,
        {
            "headline": room_type.description,
            "short_description": room_type.description,
            "room_size": "35 m2",
            "view": "View khu nghỉ dưỡng",
            "services": ["Dọn phòng mỗi ngày", "Hỗ trợ lễ tân 24/7"],
            "amenities": [item.strip() for item in room_type.amenities.split(",") if item.strip()],
            "rules": [
                "Không hút thuốc trong phòng",
                "Nhận phòng từ 14:00, trả phòng trước 12:00",
                f"Phù hợp tối đa {room_type.capacity} người lớn",
            ],
            "gallery": [
                {
                    "image": ROOM_IMAGE_MAP.get(room_key),
                    "title": f"Không gian {room_type.name}",
                    "position": "center center",
                }
            ],
        },
    )
    return render(
        request,
        "room_type_detail.html",
        {
            "room_type": room_type,
            "detail": detail,
            "back_url": "/#rooms-section",
            "booking_url": "/book/",
        },
    )


@login_required(login_url="/login/")
def staff_home(request):
    if not request.user.is_staff:
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect("home")

    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.exclude(status__in=[CANCELLED_STATUS, CHECKED_IN_STATUS]).count()
    available_rooms = Room.objects.filter(status="available").count()
    occupied_rooms = Room.objects.filter(status="occupied").count()
    bookings = Booking.objects.all().order_by("-created_at")

    return render(
        request,
        "staff_home.html",
        {
            "bookings": bookings,
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "available_rooms": available_rooms,
            "occupied_rooms": occupied_rooms,
        },
    )


@login_required(login_url="/login/")
def staff_bookings(request):
    if not request.user.is_staff:
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect("home")

    room_types = RoomType.objects.all()
    status = request.GET.get("status", "")
    room_type_id = request.GET.get("room_type", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    bookings = Booking.objects.all()
    if status:
        bookings = bookings.filter(status=status)
    if room_type_id:
        bookings = bookings.filter(room__room_type__id=room_type_id)
    if date_from:
        bookings = bookings.filter(check_in__date__gte=date_from)
    if date_to:
        bookings = bookings.filter(check_out__date__lte=date_to)
    bookings = bookings.order_by("-created_at")

    context = {
        "bookings": bookings,
        "room_types": room_types,
        "selected_status": status,
        "selected_room_type": room_type_id,
        "selected_date_from": date_from,
        "selected_date_to": date_to,
        "statuses": Booking.objects.values_list("status", flat=True).distinct(),
    }
    return render(request, "staff_bookings.html", context)


@login_required(login_url="/login/")
def staff_rooms(request):
    if not request.user.is_staff:
        messages.error(request, "Bạn không có quyền truy cập trang này.")
        return redirect("home")

    room_types = RoomType.objects.all().order_by("base_price")
    if request.method == "POST":
        updated = False
        for room_type in room_types:
            price_key = f"price_{room_type.id}"
            new_price = request.POST.get(price_key)
            if new_price is not None and new_price != "" and int(new_price) != room_type.base_price:
                room_type.base_price = int(new_price)
                room_type.save()
                updated = True
        if updated:
            messages.success(request, "Đã cập nhật giá phòng thành công!")
        else:
            messages.info(request, "Không có thay đổi nào được lưu.")
        return redirect("staff_rooms")
    return render(request, "staff_rooms.html", {"room_types": room_types})
