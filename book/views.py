from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from book.serializers import BookSerializer
from .models import Book
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

class BookAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # ✅ Use JWT authentication
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]
        
    def get(self, request, book_title=None, book_id=None):
        if book_title or book_id:
            # Fetch the book based on `book_title` or `book_id`
            filter_kwargs = {"title": book_title} if book_title else {"id": book_id}
            book = get_object_or_404(Book, **filter_kwargs)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=200)
        
        # If no specific book is requested, return a list of all books
        books = Book.objects.all()
        return JsonResponse(list(books.values()), safe=False, status=200)

    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Book created!"
            }, status=status.HTTP_201_CREATED)
        
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
    