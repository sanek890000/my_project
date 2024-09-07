from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import CommentForm

def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'article': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                return redirect('article_detail', id=article.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    return render(
        request,
        'article_detail.html',
        {'article': article, 'comments': comments, 'form': form}
    )



# Create your views here.
