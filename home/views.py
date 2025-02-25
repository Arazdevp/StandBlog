from django.shortcuts import render
from django.views.generic import FormView
from blog.models import Article
from .forms import MessageForm


def home(request):
    return render(request, "home/home.html", context={"articles": Article.objects.all()})


def sidebar(request):
    return render(request, 'includes/sidebar.html', context={"articles": Article.objects.all()})


class ContactUsView(FormView):
    form_class = MessageForm
    template_name = "home/contact_us.html"

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
