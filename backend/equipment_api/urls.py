from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('summary/', views.summary_view, name='summary'),
    path('history/', views.history_view, name='history'),
    path('report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
]
