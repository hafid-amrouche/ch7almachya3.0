
from django.contrib import admin
from django.urls import path, include
from . import notification_sending_management, token_management, views, settings, scrape
from product.views import product_ajax, delete_comment
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils import timezone


last_modified_date = timezone.now()

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin-room/', admin.site.urls),
    path('send/', notification_sending_management.send, name='send-notification'),
    path('', views.home, name='home'), 
    path('update-notifications-token-list', token_management.update_notifications_token_list, name='update-notifications-token-list'),
    path('simular-products/', views.simular_products, name='simular-products'),
    path('home-ajax/', views.home_ajax, name='home-ajax'),
    path('get-people/', views.get_people, name='get-people'),
    path('get-companies/', views.get_companies, name='get-companies'),
    path('scrape/', scrape.scrape, name='scrape'),
    path('activate-dark-mode/', views.activate_dark_mode, name='activate-dark-mode'), 
    path('deactivate-dark-mode/', views.deactivate_dark_mode, name='deactivate-dark-mode'), 
    path('check-username/', views.check_username, name='check-username'),
    path('auto-complete-suggestions/', views.auto_complete_suggestions, name='auto-complete-suggestions'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('ajax-load-notifications-messages/', views.ajax_load_notifications_messages, name="ajax-load-notifications-messages"),
    path('user<int:user_id>/', include('user.urls')),
    path('product-ajax/', product_ajax, name="product-ajax"),
    path('product/<int:user_id>/<slug:slug>-<int:product_id>/', include('product.urls')),
    path('search/', views.search, name='search'),
    path('search-ajax/', views.search_ajax, name='search-ajax'),
    path('register/', views.register, name='register'),
    path('check/', views.check),
    path('log-in/', views.login, name='login'),
    path('log-out/', views.logout, name='logout'),
    path('dashboard/', include('dashboard.urls')),
    path('messages/', include('message.urls')),
    path('notifications/',views.notifications, name='notifications'),
    path('NM-count/',views.NM_count, name='NM-count'),
    path('ajax-load-notifications/',views.ajax_load_notifications, name='ajax-load-notifications'),
    path('settings/', include('settings.urls')),
    path('category/<slug:parent>/<slug:child>/', views.category, name='category'),
    path('category-ajax/', views.category_ajax, name='category-ajax'),
    path('ajax-get-comments', views.ajax_get_comments, name='ajax-get-comments'),
    path("delete-comment/", delete_comment, name='delete-comment'),
    path('store-search/', views.store_search, name='store-search'),

  
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

