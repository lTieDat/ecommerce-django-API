from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from book.serializers import BookSerializer
from .models import Book

class BookAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, book_title=None, book_id=None):
        if book_title or book_id:
            book = get_object_or_404(Book, title=book_title) if book_title else get_object_or_404(Book, id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Book created!"}, status=status.HTTP_201_CREATED)

        return JsonResponse({
            "error_message": "Invalid data!",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, book_title):
        book = get_object_or_404(Book, title=book_title)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({
            "error_message": "Invalid data!",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
