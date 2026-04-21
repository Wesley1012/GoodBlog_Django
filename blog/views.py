from django.shortcuts import render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

def post_detail(request, year, month, day, post):
    try:
        post = Post.published.get(slug=post,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)
    except Post.DoesNotExist:
        raise Http404('Пост не найден.')

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})