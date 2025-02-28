from django.contrib.auth.models import User
from django.db import models
import uuid

from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name



class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="نویسنده")
    category = models.ManyToManyField(Category, related_name='articles', verbose_name="دسته بندی")
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان")
    body = models.TextField(verbose_name="مقاله")
    image = models.ImageField(upload_to='images/articles', verbose_name="تصیویر")
    published = models.BooleanField(default=True, verbose_name="وضعیت انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def get_category(self):
        return self.category.first()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
        return format_html('<h3 style="color= red;">فاقد تصویر</h3>')
    show_image.short_description = "تصوبر"

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"

    def get_like(self, user, article):
        self.likes.get(user=user, article=article)

    class Meta:
        ordering = ("-created",)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="مقاله")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', verbose_name="کاریر")

    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)

    body = models.TextField(verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} : {self.body[:30]}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="کاربر")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes", verbose_name="مقاله")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
        ordering = ("-created_at",)