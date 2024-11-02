from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag, Comment
from django.db.models import Q
from django.db.models import F
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

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


def posts_by_tag(request, tag):
    posts = Post.objects.filter(tags__slug=tag, status='Опубликовано')
    return render(request, 'blog.html', {'posts': posts, 'current_tag': tag})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post, status='проверено')
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def posts_by_tag(request, tag):
    tag = get_object_or_404(Tag, slug=tag)
    posts = Post.objects.filter(status='Опубликовано', tags=tag)
    return render(request, 'blog.html', {'posts': posts, 'tag': tag})

def posts_by_category(request, category):
    posts = Post.objects.filter(status='Опубликовано', category__slug=category)
    return render(request, 'blog.html', {'posts': posts, 'current_category': category})

def post_list_view(request):
    posts = Post.objects.select_related('author').prefetch_related('categories', 'tags').all()



def blog(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    advanced_filter = request.GET.get('advanced')
    if advanced_filter:
        posts = posts.filter(category__name=advanced_filter)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # (related_name) 'comments'
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views = F('views') + 1
    post.save(update_fields=['views'])

posts = (Post.objects.prefetch_related('tags').select_related('author').
select_related('category').filter(status="published"))

def blog_view(request):

    post_list = Post.objects.filter(status='published')

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': request.GET.get('search', '')
    }

    return render(request, 'blog.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            messages.success(request, 'Ваш пост был успешно создан.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'add_post.html', {'form': form, 'title': 'Создать пост'})

@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого поста.')
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш пост был успешно обновлен.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'add_post.html', {'form': form, 'title': 'Редактировать пост'})


# 1. Главная страница
class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.order_by('-created_at')[:5]  # Пример добавления последних постов
        context['popular_articles'] = Post.objects.order_by('-views')[:5]  # Пример популярных статей
        context['tags'] = Tag.objects.all()
        return context

    # 2. Страница "О нас"
    class AboutPageView(TemplateView):
        template_name = 'about.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['project_info'] = "Информация о проекте"
            context['contacts'] = "Контактные данные"
            return context

    # 3. Страница каталога блога
    class BlogCatalogView(ListView):
        model = Post
        template_name = 'blog_catalog.html'
        context_object_name = 'posts'
        paginate_by = 10  # Количество постов на странице

        def get_queryset(self):
            return Post.objects.filter(status='published')

    # 4. Страница детального отображения поста
    class PostDetailView(DetailView):
        model = Post
        template_name = 'post_detail.html'
        context_object_name = 'post'

    # 5. Страница добавления поста
    @method_decorator(login_required, name='dispatch')
    class PostCreateView(CreateView):
        model = Post
        form_class = PostForm
        template_name = 'post_form.html'
        success_url = reverse_lazy('blog_catalog')  # Пример URL-адреса перенаправления

        def form_valid(self, form):
            form.instance.author = self.request.user  # Установка автора поста
            return super().form_valid(form)

    # 6. Страница обновления поста
    @method_decorator(login_required, name='dispatch')
    class PostUpdateView(UpdateView):
        model = Post
        form_class = PostForm
        template_name = 'post_form.html'
        success_url = reverse_lazy('blog_catalog')

        def get_queryset(self):
            return super().get_queryset().filter(author=self.request.user)  # Фильтрация постов текущего пользователя

# Create your views here.