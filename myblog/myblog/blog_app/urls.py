from django.urls import path
from. import views
from .views import blog, post_by_slug


urlpatterns = [

       path('', views.main_view, name='main'),
       path('blog/', views.blog_view, name='blog'),
       path('blog/<slug:slug>/', views.post_detail_view, name='post_detail'),
       path('about/', views.about_view, name='about'),
       path('<slug:post_slug>/view/', post_by_slug, name='post_by_slug'),

   ]