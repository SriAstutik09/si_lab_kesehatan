from django.shortcuts import render, get_object_split, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core_auth.models import Peminjaman

@login_required(login_url='core_auth:login')
def dashboard_aslab(request):
    # Mengambil semua data peminjaman dari yang paling baru
    semua_peminjaman = Peminjaman.objects.all().order_by('-tanggal_pinjam')
    
    # Menghitung statistik untuk kotak info dashboard
    total_masuk = Peminjaman.objects.filter(status__in=['pending', 'verified']).count()
    total_disetujui = Peminjaman.objects.filter(status='disetujui').count()
    total_ditolak = Peminjaman.objects.filter(status='ditolak').count()
    
    context = {
        'semua_peminjaman': semua_peminjaman,
        'total_masuk': total_masuk,
        'total_disetujui': total_disetujui,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'aslab/dashboard.html', context)