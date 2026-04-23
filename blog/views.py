from django.shortcuts import render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import  ListView

class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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