from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),  
    path('shop/', views.shop, name='shop'),
    path('market/', views.market, name='market'),
    path('alert/', views.alert_view, name='alert'),
    path('contact/', views.contact, name='contact'),
    path('analyze/', views.analyze, name='analyze'),
    path('delete/<int:id>/', views.delete_analysis, name='delete_analysis'),
]
