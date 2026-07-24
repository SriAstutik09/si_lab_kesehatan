from django.urls import path
from . import views

app_name = 'kalab'

urlpatterns = [
    path('dashboard/', views.dashboard_kalab, name='dashboard'),
    path('persetujuan/<int:pinjam_id>/<str:aksi>/', views.persetujuan_kalab, name='persetujuan'),
]