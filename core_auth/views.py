from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Validasi akun ke database
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang kembali, {user.username}!')
            
            # ==================================================================
            # TEMPAT MENULISKAN KODE PENGECEKAN HAK AKSES (ROLE-BASED REDIRECT)
            # ==================================================================
            user_role = str(user.role).lower() if hasattr(user, 'role') and user.role else ''
            
            if user_role == 'aslab':
                return redirect('aslab:dashboard')
            elif user_role == 'kaleb' or user_role == 'kalab':
                return redirect('kalab:dashboard')
            elif user_role == 'mahasiswa':
                return redirect('mahasiswa:dashboard')
            else:
                # Jika akun staff/superuser atau role belum terdefinisi
                if user.is_staff or user.is_superuser:
                    return redirect('aslab:dashboard')
                return redirect('mahasiswa:dashboard')
            # ==================================================================
            
        else:
            messages.error(request, 'Username atau Password salah!')
            
    return render(request, 'auth/login.html')