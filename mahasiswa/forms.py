from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from core_auth.models import (
    Peminjaman,
    DetailPeminjaman,
    RuangLab,
    AlatBahan
)

WAKTU_CHOICES = [
    (f'{jam:02d}:00', f'{jam:02d}:00')
    for jam in range(24)
]
class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman

        fields = [
            'ruang_lab',
            'keperluan',
            'nama_dosen',
            'mata_kuliah',
            'tanggal_pinjam',
            'wkt_mulai',
            'wkt_akhir'
        ]

        widgets = {
            'ruang_lab': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'keperluan': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Contoh: Praktikum Anatomi'
                }
            ),

            'nama_dosen': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nama Dosen Pengampu'
                }
            ),

            'mata_kuliah': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nama Mata Kuliah'
                }
            ),

            'tanggal_pinjam': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': timezone.localdate().isoformat()
                }
            ),

            'wkt_mulai': forms.Select(
                choices=WAKTU_CHOICES,
                attrs={
                    'class': 'form-select'
                }
            ),

            'wkt_akhir': forms.Select(
                choices=WAKTU_CHOICES,
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def clean_tanggal_pinjam(self):
        tanggal = self.cleaned_data['tanggal_pinjam']

        if tanggal < timezone.localdate():
            raise forms.ValidationError(
                'Tanggal peminjaman kadaluwarsa'
            )
        return tanggal


class DetailPeminjamanForm(forms.ModelForm):
    class Meta:
        model = DetailPeminjaman

        fields = [
            'alat_bahan',
            'jumlah'
        ]

        widgets = {
            'alat_bahan': forms.Select(
                attrs={
                    'class': 'form-select alat-select'
                }
            ),

            'jumlah': forms.NumberInput(
                attrs={
                    'class': 'form-control jumlah-input',
                    'min': 1,
                    'placeholder': 'Jumlah'
                }
            ),
        }


DetailPeminjamanFormSet = inlineformset_factory(
    Peminjaman,
    DetailPeminjaman,
    form=DetailPeminjamanForm,
    extra=1,
    can_delete=True
)