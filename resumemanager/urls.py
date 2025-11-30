from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('candidature/', views.application_form, name='application_form'),
    path('confirmation/<str:reference>/', views.confirmation, name='confirmation'),
]
