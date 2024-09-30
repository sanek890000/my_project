from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag

def main_view(request):
    return render(request, 'main.html')
def blog_view(request):
    return render(request, 'blog.html')

def post_detail_view(request, slug):
    return render(request, 'post_detail.html')


def about_view(request):
    user_count = 100
    return render(request, 'about.html', {'user_count': user_count})


def blog(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})


def post_by_slug(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.views += 1
    post.save()
    return render(request, 'post_detail.html', {'post': post})

def blog_catalog(request):
    posts = Post.objects.filter(status='published').order_by('-published_date')
    return render(request, 'blog/blog_catalog.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status='published').order_by('-published_date')
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.filter(status='published').order_by('-published_date')
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'posts': posts})

# Create your views here.
