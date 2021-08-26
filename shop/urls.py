from django.urls import path
from shop import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [

    # AUTH URLS
    path('', views.HomeView.as_view(), name="home"),
    path('category/', views.shopCategory.as_view(), name="category"),
    path('product/<int:pk>/', views.SingleProduct.as_view(), name="product"),
    path('basic/', views.basic, name="basic"),
    path('profile/', views.profile_view.as_view(), name="profile"),
    
    
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('cart/', views.cart_view, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
    path('checkout/', views.checkoutView.as_view(), name="checkout"),
    path('checkout/confirmation/', views.confirmation.as_view(), name="confirmation"),
    path('checkout/confirmation/invoice/', views.render_to_pdf, name="invoice"),
    path('search/', views.searchView, name="search"),


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='shop/password_change.html'), 
        name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'),
     name='password_reset_complete'),
]


