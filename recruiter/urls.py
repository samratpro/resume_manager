from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.recruiter_login, name='recruiter_login'),
    path('logout/', views.recruiter_logout, name='recruiter_logout'),
    path('dashboard/', views.dashboard, name='recruiter_dashboard'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
]
