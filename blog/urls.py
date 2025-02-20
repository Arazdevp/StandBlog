from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_list, name="articles"),
    path('search', views.search, name="search_article"),
    path('category/<str:name>', views.category_details, name="category_details"),
    path('<slug:slug>', views.article_details, name="article_detail"),
]