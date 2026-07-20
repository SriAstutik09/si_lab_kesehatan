from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ==========================================
# 1. MODEL USER (CUSTOM USER MODEL)
# ==========================================
class User(AbstractUser):
    ROLE_CHOICES = [
        ('mahasiswa', 'Mahasiswa/PJMK'),
        ('aslab', 'Asisten Laboratorium'),
        ('kaleb', 'Kepala Laboratorium'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='mahasiswa')
    nim = models.CharField(max_length=20, blank=True, null=True, unique=True)
    prodi = models.CharField(max_length=50, blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ==========================================
# 2. MODEL RUANG LABORATORIUM
# ==========================================
class RuangLab(models.Model):
    nama_ruang = models.CharField(max_length=100)
    kapasitas = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama_ruang


# ==========================================
# 3. MODEL ALAT & BAHAN
# ==========================================
class AlatBahan(models.Model):
    nama_alat = models.CharField(max_length=100)
    stok_tersedia = models.IntegerField(default=0)
    satuan = models.CharField(max_length=20, default='Pcs')

    def __str__(self):
        return f"{self.nama_alat} ({self.stok_tersedia} {self.satuan})"


# ==========================================
# 4. MODEL PEMINJAMAN LAB (TRANSAKSI UTAMA)
# ==========================================
class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Validasi ASLAB'),
        ('verified', 'Menunggu Persetujuan KALAB'),
        ('disetujui', 'Disetujui / Jadwal Dikunci'),
        ('ditolak', 'Ditolak'),
        ('selesai', 'Selesai / Sudah Dikembalikan'),
    ]

    # Aktor & Logistik
    mahasiswa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='peminjaman_mahasiswa')
    ruang_lab = models.ForeignKey(RuangLab, on_delete=models.CASCADE)
    alat_bahan = models.ForeignKey(AlatBahan, on_delete=models.PROTECT)
    
    # Detail Keperluan Form
    keperluan = models.TextField()
    nama_dosen = models.CharField(max_length=100)
    mata_kuliah = models.CharField(max_length=100)
    
    # Pengendalian Waktu/Jadwal
    tanggal_pinjam = models.DateField()
    wkt_mulai = models.TimeField()
    wkt_akhir = models.TimeField()
    
    # Validasi Tracing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    di_validasi_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='aslab_verifikator'
    )
    tgl_pengajuan = models.DateTimeField(auto_now_add=True)
    catatan_tolak = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mahasiswa.username} - {self.ruang_lab.nama_ruang} ({self.tanggal_pinjam})"


# ==========================================
# 5. MODEL REKAPITULASI LAPORAN
# ==========================================
class LaporanRekap(models.Model):
    STATUS_LAPORAN = [
        ('draft', 'Draft Laporan'),
        ('dikirim', 'Menunggu Review KALAB'),
        ('revisi', 'Perlu Revisi'),
        ('approved', 'Approved / Masuk Riwayat'),
    ]

    judul_laporan = models.CharField(max_length=150)
    dibuat_oleh = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aslab_pembuat')
    konten_rekap = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_LAPORAN, default='draft')
    ulasan_revisi = models.TextField(blank=True, null=True)
    tgl_dibuat = models.DateTimeField(auto_now_add=True)
    tgl_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.judul_laporan} - Status: {self.get_status_display()}"