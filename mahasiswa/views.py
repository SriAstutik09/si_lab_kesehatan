from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core_auth.models import Peminjaman, RuangLab, AlatBahan
from .forms import PeminjamanForm

@login_required(login_url='core_auth:login')
def dashboard_view(request):
    jadwal_mahasiswa = Peminjaman.objects.filter(mahasiswa=request.user).order_by('-tanggal_pinjam')
    total_menunggu = Peminjaman.objects.filter(mahasiswa=request.user, status__in=['pending', 'verified']).count()
    total_disetujui = Peminjaman.objects.filter(mahasiswa=request.user, status='disetujui').count()
    total_ditolak = Peminjaman.objects.filter(mahasiswa=request.user, status='ditolak').count()
    
    context = {
        'jadwal_mahasiswa': jadwal_mahasiswa,
        'total_menunggu': total_menunggu,
        'total_disetujui': total_disetujui,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'mahasiswa/dashboard.html', context)

@login_required(login_url='core_auth:login')
def pinjam_lab_view(request):
    # OTOMATIS MENGISI DATA DENGAN MENYERTAKAN KAPASITAS
    if not RuangLab.objects.exists():
        RuangLab.objects.create(nama_ruang="Lab Atas", kapasitas=30)  # Sesuaikan dengan field modelmu
        RuangLab.objects.create(nama_ruang="Lab Bawah", kapasitas=30)
        
    if not AlatBahan.objects.exists():
        AlatBahan.objects.create(nama_alat="Stetoskop & Tensimeter")
        AlatBahan.objects.create(nama_alat="Manekin Anatomi Kesehatan")
        AlatBahan.objects.create(nama_alat="Set Bedah Minor / Hecting Kit")

    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            peminjaman = form.save(commit=False)
            peminjaman.mahasiswa = request.user
            peminjaman.status = 'pending'
            peminjaman.save()
            messages.success(request, 'Pengajuan peminjaman berhasil dikirim! Menunggu validasi ASLAB.')
            return redirect('mahasiswa:dashboard')
    else:
        form = PeminjamanForm()
    
    return render(request, 'mahasiswa/form_pinjam.html', {'form': form})