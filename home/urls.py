from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sidebar', views.sidebar, name='sidebar_partial'),
    path('contact', views.ContactUsView.as_view(), name='contact_us'),
]