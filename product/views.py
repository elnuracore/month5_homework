from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Review, Product, Category
from django.db import transaction
from .serializers import (
    CategoryListSerializers,
    ProductListSerializers,
    ReviewListSerializers,
    ProductReviewsSerializer,
    CategoryDetailSerializer,
    CategoryValidationSerializer,
    ProductsValidationSerializer,
    ReviewsValidationSerializer
)
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination


class CategoryListAPIView(ListCreateAPIView):
    serializer_class = CategoryListSerializers
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination

# @api_view(['GET', 'POST'])

# def categories_api_view(request):

#     if request.method == "GET":
#         categories = Category.objects.all()
#         data = CategoryListSerializers(categories, many=True).data
#         return Response(data=data)
    
#     elif request.method == "POST":
#         serializer = CategoryValidationSerializer(data=request.data)
#         serializer.is_valid(raise_exception = True)
#         name = serializer.validated_data.get('name')

#     with transaction.atomic():

#         categories = Category.objects.create(
#         name=name
#         )
#         categories.save()
#         return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializers(categories).data)

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    pagination_class = PageNumberPagination

# @api_view(['GET', "PUT", "DELETE"])

# def category_detail_api_view(request, id):

#     try:

#         category = Category.objects.get(id=id)

#     except Category.DoesNotExist:

#         return Response(status=status.HTTP_404_NOT_FOUND, data={"error" : "category not found"})

#     if request.method == "GET":

#          data = CategoryDetailSerializer(category).data
#          return Response(data=data)
    

#     elif request.method == "PUT":
#         serializers = CategoryValidationSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)

#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#     with transaction.atomic():
#         category.name = request.data.get('name')
#         category.save()
#         return Response(status=status.HTTP_201_CREATED, data = CategoryDetailSerializer(category).data)



class ProductsAPIView(ModelViewSet):
    serializer_class = ProductListSerializers
    queryset = Product.objects.all()
    lookup_field = 'id'
    pagination_class = PageNumberPagination

# @api_view(['GET', 'POST'])

# def products_api_view(request):
#     if request.method == "GET":
#         products = Product.objects.select_related('category').all()
#         data = ProductListSerializers(products, many=True).data
#         return Response(data=data)

#     elif request.method == "POST":
#         serializers = ProductsValidationSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         product = Product.objects.create(
#         title = serializers.validated_data.get('title'),
#         description = serializers.validated_data.get('description'),
#         price = serializers.validated_data.get('price'),
#         category_id = serializers.validated_data.get('category_id')
#     )
#     return Response(status=status.HTTP_201_CREATED, data=ProductListSerializers(product).data)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductListSerializers
    queryset = Product.objects.all()
    lookup_field = "id"


# @api_view(['GET', "PUT", "DELETE"])
# def product_detail_api_view(request, id):
#     try:
#         products = Product.objects.get(id=id)

#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
  
#     if request.method == "GET":
#         data = ProductListSerializers(products).data
#         return Response(data=data)
    
#     elif request.method == "PUT":
#         serializers = ProductsValidationSerializer(data=request.data)
#         serializers.is_valid(raise_exception = True)
#         products.title = serializers.validated_data.get('title')
#         products.description = serializers.validated_data.get('description')
#         products.price = serializers.validated_data.get('price')
#         products.category_id=serializers.validated_data.get("category_id")
#         products.save()
#         return Response(status=status.HTTP_201_CREATED, data=ProductListSerializers(products).data)

#     elif request.method == "DELETE":
#         products.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewListSerializers
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination

# @api_view(['GET', 'POST'])
# def reviews_api_view(request):

#     if request.method == "GET":
#         reviews = Review.objects.prefetch_related('product').all()
#         data = ReviewListSerializers(reviews, many=True).data
#         return Response(data=data)

#     elif request.method == "POST":
#         serializers = ReviewsValidationSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         text = serializers.validated_data.get('text')
#         rate = serializers.validated_data.get('rate')
#         product = serializers.validated_data.get('product')

#     with transaction.atomic():
#         reviews = Review.objects.create(
#         text = text,
#         rate = rate
#         )
#         reviews.product.set(product)
#         return Response(status=status.HTTP_201_CREATED, data = ReviewListSerializers(reviews).data)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewListSerializers
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'

# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)

#     except Review.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
#     if request.method == "GET":
#         data = ReviewListSerializers(review).data
#         return Response(data=data)

#     elif request.method == 'PUT':
#         serialializers = ReviewsValidationSerializer(data=request.data)
#         serialializers.is_valid(raise_exception=True)
#         review.text = serialializers.validated_data.get('text')
#         review.rate = serialializers.validated_data.get('rate')
#         review.save()
#         review.product.set(serialializers.validated_data.get("product"))
#         return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializers(review).data)
    
#     elif request.method == "DELETE":
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



class ProductReviewsListAPIView(ListAPIView):
    serializer_class = ProductReviewsSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination

# @api_view(['GET'])

# def product_reviews_list_view(request):

#     products = Product.objects.prefetch_related('reviews').all()

#     data = ProductReviewsSerializer(products, many=True).data

#     return Response(data=data)


# @api_view(['GET'])

# def category_list_api_view(request, id):
#     try:
#         category = Category.objects.get(id=id)

#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Category not found'})

#     data = CategoryListSerializers(category).data
#     return Response(data=data)




