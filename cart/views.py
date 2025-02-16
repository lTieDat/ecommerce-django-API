from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cart.models import Cart
from customer.models import Customer
from book.models import Book
from .serializers import CartSerializer
from rest_framework.response import Response
import requests

class CartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    CUSTOMER_API_URL = "http://127.0.0.1:8000/api/customers/"
    BOOK_API_URL = "http://127.0.0.1:8000/api/books/"

    def get_jwt_token(self, request):
        """Extract the JWT token from the request's authorization header."""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    def fetch_data_from_api(self, url, token):
        """Fetch data from a given API endpoint with the provided JWT token."""
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.RequestException:
            return None

    def get(self, request, customer_name=None):
        token = self.get_jwt_token(request)
        if not token:
            return Response({"error": "Authentication token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        if customer_name:
            # Split customer_name into first and last names
            name_parts = customer_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else None
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None

            # Get the customer from the customer service
            customers_url = f"{self.CUSTOMER_API_URL}?first_name={first_name}&last_name={last_name}"
            customer_data = self.fetch_data_from_api(customers_url, token)
            if not customer_data or len(customer_data) == 0:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            customer_id = customer_data[0]["id"]

            # Get the cart for the customer
            carts = Cart.objects.filter(customer_id=customer_id)
            if not carts.exists():
                return Response({"error": "No cart found for the given customer name"}, status=status.HTTP_404_NOT_FOUND)

            # Build response data
            cart_data = []
            for cart in carts:
                book_url = f"{self.BOOK_API_URL}{cart.book_id}/"
                book_data = self.fetch_data_from_api(book_url, token)
                if not book_data:
                    return Response({"error": f"Book with ID {cart.book_id} not found"}, status=status.HTTP_404_NOT_FOUND)

                cart_data.append({
                    "id": cart.id,
                    "customer": customer_data[0],  # Include customer object
                    "book": book_data,  # Include book object
                    "quantity": cart.quantity,
                })

            return Response(cart_data, status=status.HTTP_200_OK)

        else:
            # If no customer name is provided, fetch all carts
            carts = Cart.objects.all()
            cart_data = []

            for cart in carts:
                # Fetch customer data
                customer_url = f"{self.CUSTOMER_API_URL}{cart.customer_id}/"
                print(customer_url)
                customer_data = self.fetch_data_from_api(customer_url, token)
                print(customer_data)
                if not customer_data:
                    return Response({"error": f"Customer with ID {cart.customer_id} not found"}, status=status.HTTP_404_NOT_FOUND)

                # Fetch book data
                book_url = f"{self.BOOK_API_URL}{cart.book_id}/"
                book_data = self.fetch_data_from_api(book_url, token)
                if not book_data:
                    return Response({"error": f"Book with ID {cart.book_id} not found"}, status=status.HTTP_404_NOT_FOUND)

                cart_data.append({
                    "id": cart.id,
                    "customer": customer_data,  # Include customer object
                    "book": book_data,  # Include book object
                    "quantity": cart.quantity,
                })

            return Response(cart_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add a new item to the cart.
        """
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cart_id):
        """
        Update an existing cart item.
        """
        cart = get_object_or_404(Cart, id=cart_id)
        serializer = CartSerializer(cart, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cart_id):
        """
        Delete a cart item by its ID.
        """
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
        return Response({"message": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
