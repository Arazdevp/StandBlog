from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sidebar', views.sidebar, name='sidebar_partial'),
    path('contact', views.contact_us, name='contact_us'),
]