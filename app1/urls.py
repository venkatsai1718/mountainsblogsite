from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('newblog/', views.newpost, name='newpost'),
    path('myblogs/', views.myblogs, name='myblogs'),
    path('editblog/<int:pk>', views.editblog, name='editblog'),
    path('deleteblog/<int:pk>', views.delete_blog, name='delete_blog'),
]