# ==============================================================================
# IMPOR MODUL DAN DEPENDENSI DJANGO
# ==============================================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core_auth.models import Peminjaman


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

    # Mengambil peminjaman buatan Mahasiswa asli (mengabaikan jika ada pengajuan dummy dari akun ASLAB)
    semua_peminjaman = Peminjaman.objects.exclude(mahasiswa__username__icontains='aslab').order_by('-tanggal_pinjam')
    
    # Penghitungan Statistik Ringkasan
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
# 2. VIEW AKSI VERIFIKASI / TOLAK / SELESAI PENGEMBALIAN
# ==============================================================================
@login_required(login_url='core_auth:login')
def verifikasi_peminjaman(request, pinjam_id, aksi):
    """
    Fungsi aksi tombol ASLAB untuk mengubah status transaksi:
    - verifikasi : pending -> verified (oper ke KALAB)
    - tolak      : pending/verified -> ditolak
    - selesai    : pengembalian_diajukan -> selesai
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

    # Ambil semua data peminjaman milik mahasiswa
    laporan_list = Peminjaman.objects.exclude(mahasiswa__username__icontains='aslab').order_by('-tanggal_pinjam')

    # Filter berdasarkan tanggal jika parameter diisi
    if tgl_mulai and tgl_selesai:
        laporan_list = laporan_list.filter(tanggal_pinjam__range=[tgl_mulai, tgl_selesai])

    # Hitung ringkasan statistik laporan
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