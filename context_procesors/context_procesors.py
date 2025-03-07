from blog.models import Article
from blog.models import Category


def recent_articles(request):
    return {"recent_articles": Article.objects.order_by('-created')[:3], "categories": Category.objects.all()}