from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Book, Review
from .serializers import BookListSerializer, ReviewSerializer, BookDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'author', 'publication_date']


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class ReviewList(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.request.data.get('book', None)
        book = Book.objects.get(id=book_id)
        serializer.save(user=self.request.user, book=book)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
