from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name="articles"),
    path('add', views.AddArticleView.as_view(), name="add_article"),
    path('search', views.search, name="search_article"),
    path('category/<str:name>', views.category_details, name="category_details"),
    path('like/<slug:slug>/<int:pk>', views.like, name="like"),
    path('<slug:slug>', views.ArticleDetailsView.as_view(), name="article_detail"),
]