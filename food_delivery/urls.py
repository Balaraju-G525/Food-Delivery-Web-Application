from django.contrib import admin
from django.urls import path
from restaurants import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("restaurant/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("food/<int:food_id>/", views.food_detail, name="food_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:food_id>/", views.update_cart, name="update_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
]
