from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "price", "stock"]
        extra_kwargs = {
            "stock": {"read_only": True},
        }

