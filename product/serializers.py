from rest_framework import serializers
from .models import Review, Category, Product
from rest_framework.exceptions import ValidationError

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

class CategoryValidationSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=255)

class ProductsValidationSerializer(serializers.Serializer):
    title = serializers.CharField(min_length = 1, max_length = 255)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(min_value=1, max_value=5000)
    category_id = serializers.ListField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist')
        return category_id

class ReviewsValidationSerializer(serializers.Serializer):
    text = serializers.CharField(min_length = 1, max_length = 255, required=False)
    rate = serializers.IntegerField(min_value=1, max_value=10, required=True)
    product = serializers.ListField(child=serializers.IntegerField(), required=True, min_length=1)

    def validate_product(self, product):
        try:
            Review.objects.get(id=product)
        except:
            raise ValidationError('Product does not exist')
        return product


