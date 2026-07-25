from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

# KUNCI: Mengambil model User aktif (Custom User core_auth.User)
User = get_user_model()

def logout_view(request):
    logout(request)
    return redirect('core_auth:login')

def login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Cek apakah username/NIM ada tapi belum diaktifkan ASLAB
        user_check = User.objects.filter(username=username_input).first()
        if user_check and not user_check.is_active:
            messages.warning(request, 'Akun Anda belum aktif! Silakan tunggu verifikasi/persetujuan dari ASLAB.')
            return render(request, 'auth/login.html')

        # Validasi autentikasi
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang kembali, {user.username}!')
            
            # Pengecekan role pengguna
            user_role = str(user.role).lower() if hasattr(user, 'role') and user.role else ''
            
            if user_role == 'aslab':
                return redirect('aslab:dashboard')
            elif user_role in ['kaleb', 'kalab']:
                return redirect('kalab:dashboard')
            elif user_role == 'mahasiswa':
                return redirect('mahasiswa:dashboard')
            else:
                if user.is_staff or user.is_superuser:
                    return redirect('aslab:dashboard')
                return redirect('mahasiswa:dashboard')
            
        else:
            messages.error(request, 'Username atau Password salah!')
            
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        first_name_input = request.POST.get('first_name')
        password_input = request.POST.get('password')

        # 1. Cek apakah NIM/Username sudah terdaftar
        if User.objects.filter(username=username_input).exists():
            messages.error(request, 'NIM/Username sudah terdaftar dalam sistem!')
            return render(request, 'auth/register.html')

        # 2. Buat user baru menggunakan Custom User Model
        # Set is_active=False agar akun belum bisa digunakan sebelum di-ACC ASLAB
        user = User.objects.create_user(
            username=username_input,
            first_name=first_name_input,
            password=password_input,
            is_active=False
        )

        # 3. Set role mahasiswa jika atribut 'role' tersedia pada Custom User
        if hasattr(user, 'role'):
            user.role = 'mahasiswa'
            user.save()

        messages.success(request, 'Pendaftaran berhasil! Akun Anda sedang dalam antrean verifikasi oleh ASLAB.')
        return redirect('core_auth:login')

    return render(request, 'auth/register.html')