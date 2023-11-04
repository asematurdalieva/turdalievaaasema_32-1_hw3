from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category, Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Avg
from rest_framework import status


@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == "GET":

        products = Product.objects.all()
        products_json = ProductSerializer(products, many=True).data

        return Response(data=products_json)
    elif request.method == "POST":
        print(request.data.get('text'))
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')

        product = Product.objects.create(title=title, description=description, price=price)
        product.category.set(category)
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'id': product.id, 'title': product.title})


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        product_json = ProductSerializer(product, many=False).data
        return Response(data=product_json)
    elif request.method == "PUT":
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category.set(request.data.get('category'))
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Product updated'})
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Product deleted"})


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        categories_json = CategorySerializer(categories, many=True).data

        return Response(data=categories_json)
    elif request.method == "POST":
        print(request.data.get('text'))
        name = request.data.get('name')

        category = Category.objects.create(name=name)

        return Response(status=status.HTTP_201_CREATED,
                        data={'id': category.id, 'name': category.name})


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(data={'message': 'Category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        category_json = CategorySerializer(category, many=False).data
        return Response(data=category_json)
    elif request.method == "PUT":
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Category updated'})
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Category deleted"})


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        reviews_json = ReviewSerializer(reviews, many=True).data

        return Response(data=reviews_json)
    elif request.method == "POST":
        print(request.data.get('text'))
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')

        review = Review.objects.create(text=text, stars=stars, product_id=product_id)

        return Response(status=status.HTTP_201_CREATED,
                        data={'id': review.id, 'title': review.text})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response(data={'message': 'Review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        review_json = ReviewSerializer(review, many=False).data
        return Response(data=review_json)
    elif request.method == "PUT":
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Review updated'})
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Review deleted"})


@api_view(['GET'])
def product_reviews_api_view(request):
    reviews = Review.objects.all()
    reviews_json = ReviewSerializer(reviews, many=True).data

    return Response(data=reviews_json)


@api_view(['GET'])
def average_rating_api_view(request):
    average_rating = Review.objects.aggregate(avg_rating=Avg('stars'))
    return Response({'avg_rating': average_rating['avg_rating']})
