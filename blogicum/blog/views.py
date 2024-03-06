from django.shortcuts import get_object_or_404, render

from .models import Post, Category
from .constants import MAIN_PAGE_POSTS_QUANTITY


def index(request):
    posts = Post.objects.get_published()[:MAIN_PAGE_POSTS_QUANTITY]
    return render(request, 'blog/index.html',
                  {'post_list': posts})


def post_detail(request, ident):
    post = get_object_or_404(Post.objects.get_published(), pk=ident)
    return render(request, 'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category.objects.values(
            'id', 'is_published', 'title', 'description'
        ).filter(
            is_published=True
        ),
        slug=category_slug
    )

    posts = Post.objects.get_published().filter(
        category_id=category['id']
    )

    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
