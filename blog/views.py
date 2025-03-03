from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import ArticleForm
from .models import Article, Category, Comment, Like
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.templatetags.static import static

# Create your views here.


class BaseListView(ListView):
    paginate_by = 10

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



# def articles_list(request):
#     if request.method == 'GET':
#         page = request.GET.get('page')
#
#         paginator = Paginator(Article.objects.all(), 10)
#
#         try:
#             articles = paginator.page(page)
#         except PageNotAnInteger:
#             articles = paginator.page(1)
#         except EmptyPage:
#             articles = paginator.page(paginator.num_pages)
#
#         return render(request, 'blog/articles_list.html', context={"articles": articles})

class ArticlesListView(BaseListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(published=True)



# def article_details(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     if request.method == 'POST':
#         body = request.POST.get('body')
#         parent_id = request.POST.get('parent_id')
#         Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
#
#     context = {'article': article}
#     if request.user.is_authenticated and (x:=request.user.likes.filter(article__slug=article.slug, user_id=request.user.id).exists()):
#         context['like'] = True
#     else:
#         context['like'] = False
#
#     return render(request, "blog/article_detail.html", context=context)

# class ArticleDetailsView(DetailView):
#     model = Article
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated and self.request.user.likes.filter(article__slug=self.object.slug, user_id=self.request.user.id).exists():
#             context['like'] = True
#         else:
#             context['like'] = False
#         return context


class ArticleDetailsView(DetailView):
    model = Article
    # template_name = "blog/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.likes.filter(article__slug=self.object.slug,
                                                                                 user_id=self.request.user.id).exists():
            context['like'] = True
        else:
            context['like'] = False
        context['comments'] = self.object.comments.filter(parent__isnull=True)
        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.object = self.get_object()
            body = request.POST.get('body')
            parent_id = request.POST.get('parent_id')
            comment = Comment.objects.create(
                article=self.object,
                user=request.user,
                body=body,
                parent_id=parent_id if parent_id else None
            )
            data = {
                'success': True,
                'comment': {
                    'id': comment.id,
                    'body': comment.body,
                    'username': comment.user.username,
                    'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    'profile_image_url': comment.user.profile.image.url if comment.user.profile.image else static("images/Default-Profile-picture.png"),
                    'is_reply': True if comment.parent_id else False,
                }
            }
            return JsonResponse(data)
        return JsonResponse({'success': False})

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



class AddArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.author = self.request.user

        messages.success(self.request, "Your article will be reviewed first and then published!")

        return super().form_valid(form)
