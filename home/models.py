from django.db import models

# Create your models here.

class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    text = models.TextField(verbose_name="پیام")
    email = models.EmailField(verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"