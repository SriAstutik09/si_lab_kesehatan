# SIMPEL-K
## Sistem Informasi Peminjaman Laboratorium Kesehatan

SIMPEL-K merupakan aplikasi berbasis web yang dikembangkan menggunakan **Django** untuk membantu proses peminjaman Laboratorium Kesehatan secara terkomputerisasi. Aplikasi ini menggantikan proses peminjaman yang sebelumnya dilakukan secara manual menjadi sistem digital yang lebih efektif, efisien, dan terintegrasi.

---

## 📖 Deskripsi Aplikasi

Proses peminjaman laboratorium secara manual sering menimbulkan berbagai permasalahan, seperti pengarsipan yang kurang rapi, proses verifikasi yang lambat, serta bentroknya jadwal penggunaan laboratorium.

SIMPEL-K hadir sebagai solusi untuk mengelola seluruh proses peminjaman laboratorium mulai dari:

- Registrasi dan Login Pengguna
- Pengajuan Peminjaman Laboratorium
- Upload Berkas Persyaratan
- Verifikasi oleh Asisten Laboratorium
- Persetujuan oleh Ketua Laboratorium
- Riwayat Peminjaman
- Arsip Digital
- Laporan Peminjaman

Dengan adanya sistem ini diharapkan proses administrasi peminjaman laboratorium menjadi lebih cepat, transparan, dan terdokumentasi dengan baik.

---

# 👥 Anggota Kelompok

| No | Nama | NIM |
|----|------|-------------|
| 1 | Sri Astutik Nur Alami | 2421400076 |
| 2 | Ayu Alfi Hidayati | 2421400175 |
| 3 | Rifa | 2421400009 |
| 4 | Keza Maghfira Ramadani | 2421400044 |

---

# 📌 Pembagian Tugas

### Sri Astutik Nur Alami
- Diskusi penentuan sistem
- Perancangan sistem
- Desain Database
- Desain Alur Sistem
- Backend Development

### Ayu Alfi Hidayati
- Diskusi penentuan sistem
- Perancangan sistem
- UI/UX
- Penyusunan Laporan

### Rifa
- Diskusi penentuan sistem
- Perancangan sistem
- Penyusunan Laporan

### Keza Maghfira Ramadani
- Diskusi penentuan sistem
- Perancangan sistem
- Penyusunan Laporan

---

# 👤 Role Pengguna

Aplikasi memiliki tiga jenis pengguna:

## Mahasiswa
- Registrasi
- Login
- Mengajukan peminjaman
- Upload berkas
- Melihat status peminjaman
- Pengembalian laboratorium

## Asisten Laboratorium
- Login
- Verifikasi berkas
- Mengelola master data
- Melihat seluruh pengajuan
- Menolak atau meneruskan pengajuan

## Ketua Laboratorium
- Login
- Melihat pengajuan yang telah diverifikasi
- Menyetujui peminjaman
- Menolak peminjaman

---

# ✨ Fitur Utama

- Login & Register
- Dashboard berdasarkan Role
- Pengajuan Peminjaman
- Upload Berkas Persyaratan
- Validasi Jadwal Laboratorium
- Verifikasi Berkas
- Persetujuan Peminjaman
- Riwayat Peminjaman
- Arsip Digital
- CRUD Data Ruangan
- CRUD Data Alat/Bahan
- Laporan Peminjaman
- Cetak Laporan PDF
- Jadwal Penggunaan Laboratorium

---

# 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|-----------|
| Bahasa Pemrograman | Python |
| Framework | Django |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Version Control | Git & GitHub |

---

# 📂 Struktur Alur Sistem

```text
Mahasiswa
      │
      ▼
Mengajukan Peminjaman
      │
      ▼
Upload Berkas
      │
      ▼
Validasi Jadwal
      │
      ▼
Asisten Laboratorium
(Verifikasi Berkas)
      │
      ▼
Ketua Laboratorium
(Setujui / Tolak)
      │
      ▼
Status Ditampilkan
kepada Mahasiswa
```

---

# ⚙️ Cara Instalasi

1. Clone repository

```bash
git clone https://github.com/SriAstutik09/si_lab_kesehatan.git
```

2. Masuk ke folder project

```bash
cd si_lab_kesehatan
```

3. Install dependency

```bash
pip install -r requirements.txt
```

4. Jalankan migrasi database

```bash
python manage.py migrate
```

5. (Opsional) Membuat akun administrator

```bash
python manage.py createsuperuser
```

---

# ▶️ Cara Menjalankan Aplikasi

Jalankan server Django

```bash
python manage.py runserver
```

Kemudian buka browser pada alamat

```
http://127.0.0.1:8000/
```

---

# 🔑 Akun Pengujian

| Role | Username | Password |
|------|----------|----------|
| Mahasiswa | 2421400076 | mahasiswa1 |
| Asisten Lab | aslab1 | 2421400076aslab |
| Ketua Lab | kalab1 | 2421400076kalab |

---

# 📋 Pengujian Fitur

Beberapa fitur yang telah diuji menggunakan metode **Black Box Testing** antara lain:

- Login
- Registrasi
- Pengajuan Peminjaman
- Pengembalian Laboratorium
- Verifikasi Berkas
- Persetujuan Peminjaman
- CRUD Data Ruang
- CRUD Data Alat
- Cetak Laporan PDF

Seluruh fitur utama berhasil berjalan sesuai dengan kebutuhan sistem.

---

# 🚀 Repository

GitHub Repository

https://github.com/SriAstutik09/si_lab_kesehatan

---

# 📈 Pengembangan Selanjutnya

Pengembangan yang dapat dilakukan pada versi berikutnya antara lain:

- Notifikasi Email
- Push Notification
- Export PDF & Excel
- Dashboard Statistik
- Grafik Peminjaman
- Autentikasi Dua Faktor (2FA)
- Validasi Jadwal yang Lebih Komprehensif
- Dukungan Peminjaman Lebih dari Satu Ruangan

---

# 📄 Lisensi

Project ini dibuat sebagai tugas **Ujian Akhir Semester Mata Kuliah Web Programming** Program Studi Teknik Informatika Universitas Nurul Jadid.

---

## © Kelompok 4 - SIMPEL-K
Sistem Informasi Peminjaman Laboratorium Kesehatan
