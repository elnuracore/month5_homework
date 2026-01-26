from django.shortcuts import render
from rest_framework import status
from .models import Review, Product, Category
from .serializers import (CategoryListSerializers,
                          ProductListSerializers,
                          ReviewListSerializers
                          )
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def category_list_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error':'category not found'})
    data = CategoryListSerializers(category, many=False).data
    return Response(
        data = data
    )

@api_view(['GET'])
def categories_api_view(request):
    category = Category.objects.all()
    data = CategoryListSerializers(category, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_list_api_view(request, id):
    try: 
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error':'product not found'})
    data = ProductListSerializers(product, many=False).data
    return Response(data=data)

@api_view(['GET'])
def products_api_view(request):
    product = Product.objects.all()
    data = ProductListSerializers(product, many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error":"view not found"})
    data = ReviewListSerializers(review, many=False).data
    return Response(data=data)

@api_view(['GET'])
def reviews_api_view(request):
    review = Review.objects.all()
    data = ReviewListSerializers(review, many=True).data
    return Response(data=data)