from django.shortcuts import render
from .models import Post
from django.http import Http404

def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'post': posts})

def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404('Пост не найден.')

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})