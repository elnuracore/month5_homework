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