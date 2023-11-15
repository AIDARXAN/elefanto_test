from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Book, Review


class BookListSerializer(serializers.ModelSerializer):
    detail_link = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'detail_link', 'average_rating', 'is_favorite']

    def get_detail_link(self, obj):
        request = self.context.get('request')
        return reverse('book-detail', args=[str(obj.id)], request=request)

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        return obj.is_in_favorites(user) if user else False


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class NestedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['id', 'book']


class BookDetailSerializer(BookListSerializer):
    is_favorite = serializers.SerializerMethodField()
    reviews = NestedReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'average_rating', 'is_favorite', 'reviews']


class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomRegisterSerializer(RegisterSerializer):
    username = None

