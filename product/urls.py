from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name="product"),
    path('save/', views.save_product, name="save-product"),
    path('unsave/', views.unsave_product, name="unsave-product"),
    path('comment-<int:comment_id>', views.single_comment, name="single-comment"),
    path('comment-<int:comment_id>-ajax', views.ajax_single_comment, name="ajax-single-comment"),
    path('delete/', views.delete_product, name="delete-product"),
    path("like/", views.like, name='like'),
    path("dislike/", views.dislike, name='dislike'),
    path("comment/", views.comment, name='comment'),

]
