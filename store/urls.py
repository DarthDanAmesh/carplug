from store.admin import admin_site
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('caradmin/', admin_site.urls),
    
    # Main pages
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    
    # Search and filtering
    path('search/', views.search_view, name='search'),
    path('manufacturer/<int:manufacturer_id>/', views.manufacturer_view, name='manufacturer'),
    path('carousel/', views.carousel_list, name='carousel'),
    
    # User account management
    path('accounts/login/', auth_views.LoginView.as_view(template_name='store_templates/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/', views.user_profile, name='profile'),
    
    # Reviews
    path('cars/<int:car_id>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    
    # Admin custom views (if not using Django admin)
    path('admin/cars/', views.admin_car_list, name='admin_car_list'),


    # Shop and categories
    path('shop/', views.shop_view, name='shop'),
    
    # Deals and special offers
    path('deals/', views.deals_view, name='deals'),
    
    # About and contact
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # User account related
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('orders/', views.user_orders, name='orders'),
    
    # Policy pages
    path('faq/', views.faq_view, name='faq'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)