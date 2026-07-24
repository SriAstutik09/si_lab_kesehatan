from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core_auth.models import Peminjaman


# ==============================================================================
# HELPER FUNCTION: PENGECEKAN ROLE AKSES KALAB
# ==============================================================================
def cekk_role_kalab(user):
    username_lower = user.username.lower()
    if 'aslab' in username_lower:
        return 'aslab:dashboard'
    elif 'kalab' not in username_lower and not user.groups.filter(name__iexact='KALAB').exists():
        return 'mahasiswa:dashboard'
    return None


# ==============================================================================
# 1. VIEW DASHBOARD KALAB
# ==============================================================================
@login_required(login_url='core_auth:login')
def dashboard_kalab(request):
    """
    Menampilkan daftar pengajuan yang SUDAH DIVERIFIKASI ASLAB (verified) 
    untuk disetujui (ACC) atau ditolak oleh Kepala Lab.
    """
    target = cekk_role_kalab(request.user)
    if target:
        return redirect(target)

    # Hanya ambil data peminjaman yang berstatus 'verified' (antrean persetujuan KALAB)
    antrean_persetujuan = Peminjaman.objects.filter(status='verified').order_by('-tanggal_pinjam')
    
    # Riwayat peminjaman yang sudah diproses oleh KALAB maupun keseluruhan
    riwayat_peminjaman = Peminjaman.objects.filter(status__in=['disetujui', 'selesai', 'ditolak']).order_by('-tanggal_pinjam')

    # Statistik Ringkasan Dashboard KALAB
    total_butuh_acc = antrean_persetujuan.count()
    total_disetujui = Peminjaman.objects.filter(status__in=['disetujui', 'selesai']).count()
    total_ditolak = Peminjaman.objects.filter(status='ditolak').count()

    context = {
        'antrean_persetujuan': antrean_persetujuan,
        'riwayat_peminjaman': riwayat_peminjaman,
        'total_butuh_acc': total_butuh_acc,
        'total_disetujui': total_disetujui,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'kalab/dashboard.html', context)


# ==============================================================================
# 2. VIEW AKSI PERSETUJUAN (ACC / TOLAK) KALAB
# ==============================================================================
@login_required(login_url='core_auth:login')
def persetujuan_kalab(request, pinjam_id, aksi):
    """
    Fungsi persetujuan final oleh KALAB:
    - acc   : verified -> disetujui
    - tolak : verified -> ditolak
    """
    target = cekk_role_kalab(request.user)
    if target:
        return redirect(target)

    peminjaman = get_object_or_404(Peminjaman, id=pinjam_id)

    if aksi == 'acc':
        peminjaman.status = 'disetujui'
        messages.success(request, f'Pengajuan peminjaman oleh {peminjaman.mahasiswa.username} telah DISETUJUI!')
    elif aksi == 'tolak':
        peminjaman.status = 'ditolak'
        messages.error(request, f'Pengajuan peminjaman oleh {peminjaman.mahasiswa.username} DITOLAK.')

    peminjaman.save()
    return redirect('kalab:dashboard')