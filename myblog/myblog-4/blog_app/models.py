from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/category/{self.slug}/"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.lower())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/tag/{self.slug}/"

class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', null=True, default=None)
    tags = models.ManyToManyField(Tag, related_name='posts')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/post/{self.slug}/"

class Comment(models.Model):
    STATUS_CHOICES = (
        ('checked', 'Проверено'),
        ('unchecked', 'Не проверено')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unchecked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"
