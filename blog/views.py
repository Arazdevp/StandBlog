from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

def articles_list(request):
    if request.method == 'GET':
        page = request.GET.get('page')

        paginator = Paginator(Article.objects.all(), 10)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return render(request, 'blog/articles_list.html', context={"articles": articles})


def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
    return render(request, "blog/article_details.html", context={"article": article})



def category_details(request, name):
    category = get_object_or_404(Category, name=name)
    articles = category.articles.all()
    return render(request, "blog/articles_list.html", context={"articles": articles})


def search(request):
    q = request.GET.get('q')

    page = request.GET.get('page')

    paginator = Paginator(Article.objects.filter(title__icontains=q), 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, "blog/articles_list.html", context={"articles": articles})

