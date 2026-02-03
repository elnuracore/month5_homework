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

@api_view(['GET', 'POST'])
def categories_api_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        data = CategoryListSerializers(categories, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(data=CategoryListSerializers(category).data, status=status.HTTP_201_CREATED)    
    
        

@api_view(['GET'])
def category_list_api_view(request, id): 
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Category not found'})
    data = CategoryListSerializers(category).data
    return Response(data=data)

@api_view(['GET', 'POST'])
def products_api_view(request):
    if request.method == "GET":
        products = Product.objects.select_related('category').all()
        data = ProductListSerializers(products, many=True).data
        return Response(data=data)
    
    elif request.method == "POST":
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        categories = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id = category_id
        )
        return Response(data=ProductListSerializers(categories).data, status=status.HTTP_201_CREATED)



@api_view(['GET', "PUT", "DELETE"])
def product_detail_api_view(request, id):
    try: 
        products = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})
    
    if request.method == 'GET':
        data = ProductListSerializers(products).data
        return Response(data=data)
    
    elif request.method == "PUT":
        products.text = request.data.get('text')
        products.rate = request.data.get('rate')
        products.product.set(request.data.get('product'))
        products.save()

        return Response(data=ProductListSerializers(products).data, status=status.HTTP_201_CREATED)
   
    elif request.method == "DELETE":
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', "POST"])
def reviews_api_view(request):
    if request.method == "GET":
        reviews = Review.objects.prefetch_related('product').all()
        data = ReviewListSerializers(reviews, many=True).data
        return Response(data=data)
    
    elif request.method == "POST":
        text = request.data.get('text')
        rate = int(request.data.get('rate'))
        reviews = Review.objects.create(
            text=text,
            rate=rate
        )
        reviews.product.set(request.data.get('product'))
        return Response(data=ReviewListSerializers(reviews).data, status=status.HTTP_201_CREATED)

@api_view(['GET', "PUT", "DELETE"])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Review not found"})
    if request.method == "GET":
        data = ReviewListSerializers(review).data
        return Response(data=data)
    elif request.method == "PUT":
        review.text = request.data.get('text')
        review.rate = request.data.get('rate')
        review.product.set(request.data.get('product'))
        review.save()
        return Response(data=ReviewListSerializers(review).data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error" : "category not found"})
    if request.method == "GET":
        data = CategoryDetailSerializer(category).data
        return Response(data=data)
    
    elif request.method == "PUT":
        category.name = request.data.get('name')
        category.save()
        return Response(data=CategoryDetailSerializer(category).data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





    
