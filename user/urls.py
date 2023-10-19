from django.urls import path
from . import views
from product import views as product_views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('ajax-profile/', views.ajax_profile, name="ajax-profile"),
    path('ajax-profile-products/', views.ajax_products, name="ajax-profile-products"),
    path('report/', views.report, name="report"),
    path('follow_unfollow/', views.follow_unfollow, name="follow_unfollow"),
]
