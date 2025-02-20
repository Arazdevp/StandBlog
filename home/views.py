from django.shortcuts import render
from blog.models import Article
# Create your views here.

def home(request):
    return render(request, "home/home.html", context={"articles": Article.objects.all()})


def sidebar(request):
    return render(request, 'includes/sidebar.html', context={"articles": Article.objects.all()})