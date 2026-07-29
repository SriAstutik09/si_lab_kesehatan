from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterForm

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
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False

            if hasattr(user, 'role'):
                user.role = 'mahasiswa'

            user.save()

            messages.success(
                request,
                'Pendaftaran berhasil! Akun Anda sedang menunggu verifikasi oleh ASLAB.'
            )

            return redirect('core_auth:login')

    else:
        form = RegisterForm()

    return render(
        request,
        'auth/register.html',
        {
            'form': form
        }
    )