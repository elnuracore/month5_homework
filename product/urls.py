from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('api/v1/categories/', views.categories_api_view),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view),
    path('api/v1/products/', views.products_api_view),
    path('api/v1/products/<int:id>/', views.product_detail_api_view),
    path('api/v1/products/reviews/', views.product_reviews_list_view),
    path('api/v1/reviews/', views.reviews_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view)
]