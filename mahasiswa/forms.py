from django import forms
from core_auth.models import Peminjaman, RuangLab, AlatBahan

class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        # Field disesuaikan persis dengan model transaksi utama milikmu
        fields = [
            'ruang_lab', 
            'alat_bahan', 
            'keperluan', 
            'nama_dosen', 
            'mata_kuliah', 
            'tanggal_pinjam', 
            'wkt_mulai', 
            'wkt_akhir'
        ]
        widgets = {
            'ruang_lab': forms.Select(attrs={'class': 'form-select'}),
            'alat_bahan': forms.Select(attrs={'class': 'form-select'}),
            'keperluan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contoh: Praktikum Anatomi'}),
            'nama_dosen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Dosen Pengampu'}),
            'mata_kuliah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Mata Kuliah'}),
            'tanggal_pinjam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'wkt_mulai': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'wkt_akhir': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }