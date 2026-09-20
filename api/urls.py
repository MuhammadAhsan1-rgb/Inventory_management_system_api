from django.urls import path
from .views import ProductListCreateAPI , CategoryListCreateAPI , ProductRetrieveUpdateDestroyAPI , CategoryRetrieveUpdateDestroyAPI

urlpatterns = [
    path('categories/' , CategoryListCreateAPI.as_view()),
    path('categories/<int:pk>/' , CategoryRetrieveUpdateDestroyAPI.as_view()),
    path('products/' , ProductListCreateAPI.as_view()),
    path('products/<int:pk>' , ProductRetrieveUpdateDestroyAPI.as_view())
]
