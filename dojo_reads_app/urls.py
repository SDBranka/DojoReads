from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add_book),
    path('create_book', views.create_book),
    path('<int:book_id>', views.display_book),
    path('add_review', views.add_review),
    path('delete', views.delete_review),
]