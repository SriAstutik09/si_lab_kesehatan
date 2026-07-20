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
            
            # Pengecekan Hak Akses (Role-Based Redirect)
            if user.role == 'mahasiswa':
                return redirect('mahasiswa:dashboard')
            elif user.role == 'aslab':
                return redirect('aslab:dashboard')
            elif user.role == 'kaleb':
                return redirect('kalab:dashboard')
            else:
                return redirect('/admin/') # Jika superuser bawaan Django
        else:
            messages.error(request, 'Username atau Password salah!')
            
    return render(request, 'auth/login.html')