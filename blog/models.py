from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200,
                            verbose_name='Короткая метка',
                            unique_for_date='publish')
    body = models.TextField(verbose_name='Описание')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name='Статус')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор'
                               )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])