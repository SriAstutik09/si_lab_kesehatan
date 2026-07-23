from django.contrib import admin
# Panggil model/tabel dari file models.py
from .models import *  

# Kode di bawah ini berguna untuk mendaftarkan SEMUA tabel agar muncul di admin
from django.apps import apps

app = apps.get_app_config('core_auth')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass