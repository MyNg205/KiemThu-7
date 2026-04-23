from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import RoomType, Room, Booking, UserProfile
from django.http import HttpResponse
from datetime import date
from django import forms
import re
# Create your views here.

# Trang chủ: phân biệt staff và customer
@login_required(login_url='/login/')
def home(request):
    # Nếu là staff, redirect tới staff_home
    if request.user.is_staff:
        return redirect('staff_home')

    # Khách hàng: hiển thị trang chủ khách hàng với danh sách loại phòng
    room_types = RoomType.objects.all()
    return render(request, 'home.html', {'room_types': room_types})

# Trang đăng nhập
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        min_length=2,
        error_messages={
            'required': 'Vui lòng nhập họ tên.',
            'min_length': 'Họ tên phải có ít nhất 2 ký tự.',
            'max_length': 'Họ tên không được vượt quá 150 ký tự.',
        },
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={
            'required': 'Vui lòng nhập email.',
            'invalid': 'Email không đúng định dạng.',
        },
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        error_messages={
            'required': 'Vui lòng nhập số điện thoại.',
            'min_length': 'Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.',
            'max_length': 'Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.',
        },
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        required=False,
        error_messages={
            'invalid': 'Tuổi phải là số hợp lệ.',
            'min_value': 'Tuổi phải từ 18 trở lên.',
            'max_value': 'Tuổi không được vượt quá 100.',
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            'required': 'Vui lòng nhập mật khẩu.',
            'min_length': 'Mật khẩu phải có ít nhất 8 ký tự.',
        },
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        error_messages={
            'required': 'Vui lòng xác nhận mật khẩu.',
            'min_length': 'Mật khẩu xác nhận phải có ít nhất 8 ký tự.',
        },
    )

    def clean_full_name(self):
        full_name = ' '.join(self.cleaned_data['full_name'].split())
        if not full_name:
            raise forms.ValidationError('Vui lòng nhập họ tên.')
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError('Họ tên không được chứa chữ số.')
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email đã được sử dụng.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not phone:
            raise forms.ValidationError('Vui lòng nhập số điện thoại.')
        if not re.fullmatch(r'0\d{9}', phone):
            raise forms.ValidationError('Số điện thoại phải gồm đúng 10 chữ số, bắt đầu bằng số 0 và không được chứa chữ.')
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise forms.ValidationError('Mật khẩu phải có ít nhất 1 chữ cái và 1 chữ số.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Mật khẩu xác nhận không khớp.')
        return cleaned_data

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Tìm user bằng email
            try:
                user = User.objects.get(email=email)
                # Kiểm tra password
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Email hoặc mật khẩu không chính xác'})
            except User.DoesNotExist:
                return render(request, 'login.html', {'form': form, 'error': 'Email hoặc mật khẩu không chính xác'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].strip()
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            age = form.cleaned_data.get('age')
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=full_name,
                password=password,
            )
            UserProfile.objects.create(user=user, phone=phone, age=age)
            login(request, user)
            messages.success(request, 'Đăng ký tài khoản thành công.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# Đăng xuất
def logout_view(request):
    logout(request)
    return redirect('login')

# Trang thông tin cá nhân
@login_required(login_url='/login/')
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        profile.age = request.POST.get('age', '') or None
        profile.phone = request.POST.get('phone', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.save()
        messages.success(request, 'Lưu thông tin thành công!')
        return redirect('home')

    return render(request, 'profile.html', {'profile': profile})

# Trang lịch sử đặt phòng
@login_required(login_url='/login/')
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})

# Trang chi tiết phòng loại
@login_required(login_url='/login/')
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'room_detail.html', {'room': room})

# Trang đặt phòng
@login_required(login_url='/login/')
def book_room(request, room_id=None):
    room_types = RoomType.objects.all()
    rooms = Room.objects.filter(status='available')
    user = request.user
    selected_room = None
    selected_room_type = None

    # Nếu có room_id, lấy phòng đã chọn
    if room_id:
        selected_room = get_object_or_404(Room, id=room_id, status='available')
        selected_room_type = selected_room.room_type

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')

        # Validate room
        room = get_object_or_404(Room, id=room_id, status='available')
        # Lưu booking
        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        # Cập nhật thông tin user
        user.first_name = name
        user.save()
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.phone = phone
        profile.age = age
        profile.save()
        messages.success(request, f'✅ Đặt phòng thành công! Mã đơn: {booking.id}')
        return redirect('home')

    # Tạo list tuple cho room_types select
    room_type_choices = [(rt.id, rt.name) for rt in room_types]

    return render(request, 'book_room.html', {
        'room_types': room_type_choices,
        'rooms': rooms,
        'user': user,
        'selected_room': selected_room,
        'selected_room_type': selected_room_type,
    })

# Trang chọn phòng để đặt
@login_required(login_url='/login/')
def select_room_to_book(request):
    room_types = RoomType.objects.all()

    if request.method == 'POST':
        room_type_id = request.POST.get('room_type_id')
        if room_type_id:
            return redirect('room_detail', room_id=room_type_id)

    return render(request, 'select_room_to_book.html', {
        'room_types': room_types,
    })

# Hủy đặt phòng
@login_required(login_url='/login/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'Đã huỷ'
        booking.save()
        # Cập nhật trạng thái phòng nếu cần
        booking.room.status = 'available'
        booking.room.save()
        messages.success(request, 'Đã huỷ đặt phòng thành công.')
        return redirect('booking_history')
    return render(request, 'cancel_booking.html', {'booking': booking})

# Trang chi tiết loại phòng
@login_required(login_url='/login/')
def room_type_detail(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    rooms = room_type.rooms.filter(status='available')
    return render(request, 'room_type_detail.html', {'room_type': room_type, 'rooms': rooms})

# Trang home cho staff
@login_required(login_url='/login/')
def staff_home(request):
    # Kiểm tra nếu user là staff
    if not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')

    # Lấy thống kê
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.exclude(status__in=['Đã huỷ', 'Đã check in']).count()
    available_rooms = Room.objects.filter(status='available').count()
    occupied_rooms = Room.objects.filter(status='occupied').count()

    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'staff_home.html', {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
    })

# Trang quản lý đặt phòng của staff
@login_required(login_url='/login/')
def staff_bookings(request):
    # Kiểm tra nếu user là staff
    if not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')

    # Lấy danh sách loại phòng
    room_types = RoomType.objects.all()

    # Lấy các tham số lọc
    status = request.GET.get('status', '')
    room_type_id = request.GET.get('room_type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    bookings = Booking.objects.all()
    if status:
        bookings = bookings.filter(status=status)
    if room_type_id:
        bookings = bookings.filter(room__room_type__id=room_type_id)
    if date_from:
        bookings = bookings.filter(check_in__date__gte=date_from)
    if date_to:
        bookings = bookings.filter(check_out__date__lte=date_to)
    bookings = bookings.order_by('-created_at')

    # Truyền các giá trị đã chọn để giữ lại trên form
    context = {
        'bookings': bookings,
        'room_types': room_types,
        'selected_status': status,
        'selected_room_type': room_type_id,
        'selected_date_from': date_from,
        'selected_date_to': date_to,
        'statuses': Booking.objects.values_list('status', flat=True).distinct(),
    }
    return render(request, 'staff_bookings.html', context)

# Trang quản lý phòng của staff
@login_required(login_url='/login/')
def staff_rooms(request):
    # Kiểm tra nếu user là staff
    if not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')

    room_types = RoomType.objects.all().order_by('base_price')
    if request.method == 'POST':
        updated = False
        for rt in room_types:
            price_key = f'price_{rt.id}'
            new_price = request.POST.get(price_key)
            if new_price is not None and new_price != '' and int(new_price) != rt.base_price:
                rt.base_price = int(new_price)
                rt.save()
                updated = True
        if updated:
            messages.success(request, 'Đã cập nhật giá phòng thành công!')
        else:
            messages.info(request, 'Không có thay đổi nào được lưu.')
        return redirect('staff_rooms')
    return render(request, 'staff_rooms.html', {'room_types': room_types})
