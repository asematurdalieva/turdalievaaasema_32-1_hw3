from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.product_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()

    def get_product_title(self, obj):
        return obj.product.title

    class Meta:
        model = Review
        fields = ['product_title', 'stars', 'text', 'id']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']