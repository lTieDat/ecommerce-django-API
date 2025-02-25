from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            "stock": {"read_only": True},
            "created_at": {"read_only": True},
            "image": {"required": False}
        }

