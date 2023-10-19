from django.urls import path
from . import views
urlpatterns = [
    path('your-items/', views.your_items, name="your-items"),
    path('saved-posts', views.saved_posts, name='saved-posts'),
    path('your-items-ajax/', views.your_items_ajax, name="your-items-ajax"),
    path('saved-posts-ajax/', views.saved_posts_ajax, name="saved-posts-ajax"),
    path('your-items/create-item/', views.create_item, name='create-item'),
    path('your-items/<int:product_id>/', views.edit_item, name='edit-item'),
    path('your-items/<int:product_id>/<int:image_id>/delete/', views.delete_image, name='delete-image'),
    path('ok/', views.create_item_OK, name='dashborad-ok')
]
