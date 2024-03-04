from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post, Category


def index(request):

    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:5]

    return render(request, 'blog/index.html',
                  {'post_list': posts})


def post_detail(request, ident):

    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ),
        pk=ident
    )

    return render(request, 'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug):

    ident = Category.objects.values('id').get(slug=category_slug)

    category = get_object_or_404(
        Category.objects.values(
            'is_published', 'title', 'description'
        ).filter(
            is_published=True
        ),
        pk=ident['id']
    )

    posts = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=timezone.now()
    )

    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': posts})
