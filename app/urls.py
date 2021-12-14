from django.urls import path
from . import views

urlpatterns = [
  path('',views.index, name="homepage"),
  path('exit/',views.exit, name="exit"),
  path('enter/',views.enter, name="enter"),
  path('admin_view/', views.admin_view, name="admin_view"),
  path('export/', views.export, name="export_data")
]
