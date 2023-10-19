from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.settings_profile, name='settings-profile'),
    path('email/', views.email, name='email'),
    path('delete-account/', views.delete_account, name='delete-account'),
    path('make-email/', views.make_email, name='make-email'),
    path('change-email/', views.change_email, name='change-email'),
    path('change-password', views.change_password, name="change-password"),
    path("activate-email/", views.activate_email, name='activate-email'),
    path("confirm-email-activation/<uidb64>/<token>/", views.confirm_email_activation, name='confirm-activation'),
    path("forget-password", views.forgot_password, name="forget_password"),
    path("reset-password", views.reset_password, name='reset_password'),
    path("reset-password-validation/<uidb64>/<token>/", views.reset_password_validation, name='reset_password_validation'),
]
