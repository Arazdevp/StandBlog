from django.shortcuts import render
from blog.models import Article
from .forms import MessageForm
from .models import Message


def home(request):
    return render(request, "home/home.html", context={"articles": Article.objects.all()})


def sidebar(request):
    return render(request, 'includes/sidebar.html', context={"articles": Article.objects.all()})

def contact_us(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()
    return render(request, "home/contact_us.html", context={"form": form})