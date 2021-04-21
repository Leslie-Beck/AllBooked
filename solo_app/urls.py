from django.urls import path
from . import views

urlpatterns= [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('users/create', views.create_user),
    path('users/login', views.login),
    path('users/profile', views.main_page),
    path('books/create', views.create_book),
    path('books/create_ajax', views.create_ajax),
    path('books/<int:book_id>/delete', views.delete_book),
    path('books/<int:book_id>', views.book_page),
    path('books/<int:book_id>/addReview', views.review_others_book),
    path('books/<int:book_id>/<int:review_id>/like', views.like),
    path('books/<int:book_id>/<int:review_id>/unlike', views.unlike),
    path('books/<int:book_id>/addComment/<int:review_id>', views.post_comment),
]