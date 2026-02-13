from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, Product, Category
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

class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        data = CategoryListSerializers(categories, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            category = Category.objects.create(name=serializer.validated_data.get('name'))
            return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializers(category).data)

class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        return Response(data=CategoryDetailSerializer(category).data)

    def put(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        
        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializer(category).data)

    def delete(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        data = ProductListSerializers(products, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ProductsValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=ProductListSerializers(product).data)

class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
        return Response(data=ProductListSerializers(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
        
        serializer = ProductsValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for attr, value in serializer.validated_data.items():
            setattr(product, attr, value)
        product.save()

        return Response(status=status.HTTP_201_CREATED, data=ProductListSerializers(product).data)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewListCreateAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.prefetch_related('product').all()
        data = ReviewListSerializers(reviews, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ReviewsValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data.pop('product')
        with transaction.atomic():
            review = Review.objects.create(**serializer.validated_data)
            review.product.set(product_ids)
            return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializers(review).data)

class ReviewDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Review.objects.get(id=pk)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
        return Response(data=ReviewListSerializers(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
        
        serializer = ReviewsValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data.pop('product')
        review.text = serializer.validated_data.get('text')
        review.rate = serializer.validated_data.get('rate')
        review.save()
        review.product.set(product_ids)
        
        return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializers(review).data)

    def delete(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductReviewsListAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related('reviews').all()
        data = ProductReviewsSerializer(products, many=True).data
        return Response(data=data)