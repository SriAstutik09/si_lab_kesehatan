# ==============================================================================
# IMPOR MODUL DAN DEPENDENSI DJANGO
# ==============================================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from core_auth.models import Peminjaman

# Ambil Custom User Model aktif (core_auth.User)
User = get_user_model()


# ==============================================================================
# HELPER FUNCTION: PENGECEKAN ROLE AKSES ASLAB
# ==============================================================================
def cekk_role_aslab(user):
    """
    Fungsi bantu untuk mengecek apakah user yang login BUKAN ASLAB.
    Mengecek berdasarkan username, Django Group, maupun atribut role.
    """
    username_lower = user.username.lower()
    if 'kalab' in username_lower or user.groups.filter(name__iexact='KALAB').exists() or getattr(user, 'role', '') == 'KALAB':
        return 'kalab:dashboard'
    elif not ('aslab' in username_lower or user.groups.filter(name__iexact='ASLAB').exists() or getattr(user, 'role', '') == 'ASLAB'):
        return 'mahasiswa:dashboard'
    return None


# ==============================================================================
# 1. VIEW DASHBOARD ASLAB
# ==============================================================================
@login_required(login_url='core_auth:login')
def dashboard_aslab(request):
    """
    Menampilkan statistik dan seluruh daftar peminjaman untuk diproses ASLAB.
    """
    # 🛡️ KEAMANAN: Cegah Mahasiswa / KALAB menerobos ke Dashboard ASLAB
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Anda tidak memiliki hak akses sebagai ASLAB!")
        return redirect(redirect_target)

    # Mengambil peminjaman buatan Mahasiswa asli
    semua_peminjaman = Peminjaman.objects.exclude(mahasiswa__username__icontains='aslab').order_by('-tanggal_pinjam')
    
    # Penghitungan Statistik Ringkasan Peminjaman
    total_masuk = semua_peminjaman.filter(status__in=['pending', 'pengembalian_diajukan']).count()
    total_disetujui = semua_peminjaman.filter(status__in=['verified', 'disetujui', 'selesai']).count()
    total_ditolak = semua_peminjaman.filter(status='ditolak').count()
    
    context = {
        'semua_peminjaman': semua_peminjaman,
        'total_masuk': total_masuk,
        'total_disetujui': total_disetujui,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'aslab/dashboard.html', context)


# ==============================================================================
# 2. VIEW AKSI VERIFIKASI / TOLAK / SELESAI PENGEMBALIAN PEMINJAMAN
# ==============================================================================
@login_required(login_url='core_auth:login')
def verifikasi_peminjaman(request, pinjam_id, aksi):
    """
    Fungsi aksi tombol ASLAB untuk mengubah status transaksi peminjaman lab/alat.
    """
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Aksi ditolak. Anda bukan ASLAB!")
        return redirect(redirect_target)

    peminjaman = get_object_or_404(Peminjaman, id=pinjam_id)
    
    if aksi == 'verifikasi':
        peminjaman.status = 'verified'
        messages.success(request, f'Peminjaman oleh {peminjaman.mahasiswa.username} berhasil diverifikasi! Menunggu ACC KALAB.')
    elif aksi == 'tolak':
        peminjaman.status = 'ditolak'
        messages.error(request, f'Peminjaman oleh {peminjaman.mahasiswa.username} telah ditolak.')
    elif aksi == 'selesai':
        peminjaman.status = 'selesai'
        messages.success(request, f'Pengembalian alat/lab oleh {peminjaman.mahasiswa.username} telah selesai dikonfirmasi.')
        
    peminjaman.save()
    return redirect('aslab:dashboard')


# ==============================================================================
# 3. VIEW LAPORAN PEMINJAMAN
# ==============================================================================
@login_required(login_url='core_auth:login')
def laporan_peminjaman(request):
    """
    Menampilkan halaman rekapitulasi laporan peminjaman dengan fitur filter tanggal.
    """
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Anda tidak memiliki hak akses ke Halaman Laporan!")
        return redirect(redirect_target)

    tgl_mulai = request.GET.get('tgl_mulai')
    tgl_selesai = request.GET.get('tgl_selesai')

    laporan_list = Peminjaman.objects.exclude(mahasiswa__username__icontains='aslab').order_by('-tanggal_pinjam')

    if tgl_mulai and tgl_selesai:
        laporan_list = laporan_list.filter(tanggal_pinjam__range=[tgl_mulai, tgl_selesai])

    total_laporan = laporan_list.count()
    total_selesai = laporan_list.filter(status='selesai').count()
    total_ditolak = laporan_list.filter(status='ditolak').count()

    context = {
        'laporan_list': laporan_list,
        'tgl_mulai': tgl_mulai or '',
        'tgl_selesai': tgl_selesai or '',
        'total_laporan': total_laporan,
        'total_selesai': total_selesai,
        'total_ditolak': total_ditolak,
    }
    return render(request, 'aslab/laporan.html', context)


# ==============================================================================
# 4. VIEW VERIFIKASI AKUN MAHASISWA BARU (SIDEBAR MENU KHUSUS)
# ==============================================================================
@login_required(login_url='core_auth:login')
def verifikasi_akun_mhs(request):
    """
    Menampilkan halaman khusus daftar mahasiswa yang baru mendaftar (is_active = False)
    dan riwayat mahasiswa yang sudah diaktifkan.
    """
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Anda tidak memiliki hak akses ke Halaman Verifikasi Akun!")
        return redirect(redirect_target)

    # Ambil pendaftaran mahasiswa yang belum aktif (menunggu ACC)
    antrean_mhs = User.objects.filter(is_active=False).order_by('-date_joined')
    if hasattr(User, 'role'):
        antrean_mhs = antrean_mhs.filter(role='mahasiswa')

    # Ambil daftar mahasiswa yang sudah diaktifkan
    mhs_aktif = User.objects.filter(is_active=True, is_staff=False, is_superuser=False).order_by('-date_joined')
    if hasattr(User, 'role'):
        mhs_aktif = mhs_aktif.filter(role='mahasiswa')

    context = {
        'antrean_mhs': antrean_mhs,
        'mhs_aktif': mhs_aktif,
        'total_antrean': antrean_mhs.count(),
        'total_aktif': mhs_aktif.count(),
    }
    return render(request, 'aslab/verifikasi_akun.html', context)


# ==============================================================================
# 5. VIEW AKSI SETUJUI / TOLAK PEMBUATAN AKUN MAHASISWA
# ==============================================================================
@login_required(login_url='core_auth:login')
def proses_persetujuan_akun(request, user_id, aksi):
    """
    Aksi untuk mengaktifkan (is_active = True) atau menolak (hapus akun) pendaftaran mahasiswa.
    """
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Aksi ditolak!")
        return redirect(redirect_target)

    mhs = get_object_or_404(User, id=user_id)
    nama_display = mhs.first_name if mhs.first_name else mhs.username

    if aksi == 'acc':
        mhs.is_active = True
        mhs.save()
        messages.success(request, f'Akun mahasiswa {nama_display} ({mhs.username}) berhasil diaktifkan!')
    elif aksi == 'tolak':
        mhs.delete()
        messages.error(request, f'Pendaftaran akun mahasiswa {nama_display} ({mhs.username}) telah ditolak dan dihapus.')

    return redirect('aslab:verifikasi_akun')