from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    # path('success', views.success),
    path('logout', views.logout),
    path('user/<int:user_id>', views.display_user)
]