from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Review, Product, Category
from .serializers import (
    CategoryListSerializers,
    ProductListSerializers,
    ReviewListSerializers,
    ProductReviewsSerializer,
    CategoryDetailSerializer
)

@api_view(['GET'])
def product_reviews_list_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = ProductReviewsSerializer(products, many=True).data
    return Response(data=data)

@api_view(['GET'])
def categories_api_view(request):
    categories = Category.objects.all()
    data = CategoryListSerializers(categories, many=True).data
    return Response(data=data)

@api_view(['GET'])
def category_list_api_view(request, id): 
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Category not found'})
    data = CategoryListSerializers(category).data
    return Response(data=data)

@api_view(['GET'])
def products_api_view(request):
    products = Product.objects.select_related('category').all()
    data = ProductListSerializers(products, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    try: 
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
    data = ProductListSerializers(product).data
    return Response(data=data)

@api_view(['GET'])
def reviews_api_view(request):
    reviews = Review.objects.prefetch_related('product').all()
    data = ReviewListSerializers(reviews, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
    data = ReviewListSerializers(review).data
    return Response(data=data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error" : "category not found"})
    data = CategoryDetailSerializer(category).data
    return Response(data=data)
