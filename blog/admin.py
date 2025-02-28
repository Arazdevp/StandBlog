from django.contrib import admin
from .models import Article, Category, Comment

# Register your models here.

class FilterByTitle(admin.SimpleListFilter):
    title = 'کلید ها پر ترکرار'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        return (
            ("django", "DJANGO"),
            ("python", "PYTHON"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'published', 'show_image')
    list_filter = ('published', FilterByTitle)
    search_fields = ('title',)
    exclude = ('slug',)
    inlines = (CommentInline,)

admin.site.register(Category)
admin.site.register(Comment)