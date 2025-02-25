from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cart.models import Cart
from .serializers import CartSerializer
import requests

class CartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    CUSTOMER_API_URL = "http://127.0.0.1:8000/api/customers/"
    BOOK_API_URL = "http://127.0.0.1:8000/api/books/"

    def _get_jwt_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    def _fetch_data_from_api(self, url, token):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def _get_customer_data(self, customer_id, token, query_params=None):
        url = f"{self.CUSTOMER_API_URL}{customer_id}/"
        if query_params:
            url += query_params
        return self._fetch_data_from_api(url, token)

    def _get_book_data(self, book_id, token):
        url = f"{self.BOOK_API_URL}{book_id}/"
        return self._fetch_data_from_api(url, token)

    def get(self, request, email=None):
        token = self._get_jwt_token(request)
        if not token:
            return Response({"error": "Authentication token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        customer_data = self._get_customer_data(None, token, query_params=f"?username={email}")
        if not customer_data:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        customer_id = customer_data.get("id")
        carts = Cart.objects.filter(customer_id=customer_id)
        cart_data = []

        for cart in carts:
            book_data = self._get_book_data(cart.book.id, token)
            cart_data.append({
                "id": cart.id,
                "quantity": cart.quantity,
                "customer": customer_data,
                "book": book_data,
            })

        return Response(cart_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
        return Response({"message": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)