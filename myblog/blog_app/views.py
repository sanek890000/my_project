from django.shortcuts import render


def main_view(request):
    return render(request, 'main.html')


def blog_view(request):
    return render(request, 'blog.html')


def post_detail_view(request, slug):
    return render(request, 'python_blog/post_detail.html')


def about_view(request):
    user_count = 100  # Пример переменной для страницы "О проекте"
    return render(request, 'about.html', {'user_count': user_count})

# Create your views here.
