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
    Jika Mahasiswa atau KALAB mencoba masuk, kembalikan nama redirect tujuannya.
    """
    if user.groups.filter(name='KALAB').exists() or getattr(user, 'role', '') == 'KALAB':
        return 'kalab:dashboard'
    elif not (user.groups.filter(name='ASLAB').exists() or getattr(user, 'role', '') == 'ASLAB'):
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

    # Mengambil semua data peminjaman dari yang paling baru
    semua_peminjaman = Peminjaman.objects.all().order_by('-tanggal_pinjam')
    
    # --------------------------------------------------------------------------
    # PENGHITUNGAN STATISTIK
    # --------------------------------------------------------------------------
    # 1. Antrean Masuk = Hanya yang 'pending' (butuh verifikasi) & 'pengembalian_diajukan' (butuh konfirmasi)
    total_masuk = Peminjaman.objects.filter(status__in=['pending', 'pengembalian_diajukan']).count()
    
    # 2. Disetujui = Status 'verified', 'disetujui', dan 'selesai'
    total_disetujui = Peminjaman.objects.filter(status__in=['verified', 'disetujui', 'selesai']).count()
    
    # 3. Ditolak = Status 'ditolak'
    total_ditolak = Peminjaman.objects.filter(status='ditolak').count()
    
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
    # 🛡️ KEAMANAN: Hanya ASLAB yang boleh mengeksekusi fungsi ini
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
    # 🛡️ KEAMANAN: Cegah Mahasiswa menerobos halaman Laporan
    redirect_target = cekk_role_aslab(request.user)
    if redirect_target:
        messages.error(request, "Anda tidak memiliki hak akses ke Halaman Laporan!")
        return redirect(redirect_target)

    tgl_mulai = request.GET.get('tgl_mulai')
    tgl_selesai = request.GET.get('tgl_selesai')

    # Ambil semua data peminjaman
    laporan_list = Peminjaman.objects.all().order_by('-tanggal_pinjam')

    # Filter berdasarkan tanggal jika parameter diisi oleh user
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