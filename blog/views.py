from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Article, Category, Comment, Like
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


class BaseListView(ListView):
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        try:
            context[self.context_object_name] = context['paginator'].page(page)
        except PageNotAnInteger:
            context[self.context_object_name] = context['paginator'].page(1)
        except EmptyPage:
            context[self.context_object_name] = context['paginator'].page(context['paginator'].num_pages)
        return context



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

class ArticlesListView(BaseListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'



def article_details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)

    context = {'article': article}
    if request.user.is_authenticated and (x:=request.user.likes.filter(article__slug=article.slug, user_id=request.user.id).exists()):
        context['like'] = True
    else:
        context['like'] = False

    return render(request, "blog/article_detail.html", context=context)



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

def like(request, slug, pk):
    try:
        Like.objects.get(article__slug=slug, user_id=request.user.id).delete()
        return JsonResponse({'response': 'UnLiked'})
    except:
        Like.objects.create(article_id=pk, user_id=request.user.id)
        return JsonResponse({'response': 'Liked'})

    return redirect("article_detail", slug=slug)