from django.db import models
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    @property
    def products_count(self):
        return self.products.count()

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        result = self.reviews.aggregate(Avg('rate'))
        value = result['rate__avg'] or 0
        return round(value, 1)
    

STARS = tuple((i, i) for i in range(1, 6))

class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    rate = models.IntegerField(choices=STARS, default=3, null=True)
    product = models.ManyToManyField(Product, related_name='reviews')

    def __str__(self):
        return self.text
    
    @property
    def product_names(self):
        return [i.title for i in self.product.all()]