from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('user', views.ViewUser.as_view(), name='user')
    # path('logout', views.logout.as_view(), name='logout'),
]
