from django.urls import path
from. import views

urlpatterns = [
       path('', views.main_view, name='main'),
       path('blog/', views.blog_view, name='blog'),
       path('blog/<slug:slug>/', views.post_detail_view, name='post_detail'),
       path('about/', views.about_view, name='about'),
   ]