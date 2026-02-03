from rest_framework import serializers
from .models import Review, Category, Product

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializers(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = 'id title average_rating reviews'.split()

class CategoryDetailSerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = 'id name products_count'.split()