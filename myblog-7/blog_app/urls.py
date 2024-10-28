from django.urls import path
from. import views
from .views import blog, posts_by_tag, posts_by_category, post_by_slug, blog_catalog, post_detail, category_detail, tag_detail


urlpatterns = [

       path('', views.main_view, name='main'),
       path('blog/', views.blog_view, name='blog'),
       path('blog/<slug:slug>/', views.post_detail_view, name='post_detail'),
       path('about/', views.about_view, name='about'),
       path('<slug:post_slug>/view/', post_by_slug, name='post_by_slug'),
       path('post/<slug:slug>/', views.post_detail_view, name='post_detail_by_post'),
       path('tag/<slug:tag>/', posts_by_tag, name='posts_by_tag'),
       path('category/<slug:category>/', posts_by_category, name='posts_by_category'),
       path('post/<int:id>/', post_detail, name='post_detail'),

]