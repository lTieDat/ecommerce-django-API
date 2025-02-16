from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomerAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # ✅ Use JWT authentication
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, customer_id=None):
        """Retrieve all customers or a specific customer by ID (Authentication Required)"""
        if customer_id:
            customer = get_object_or_404(Customer, id=customer_id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data.get("email")
        if Customer.objects.filter(email=email).exists():
            return JsonResponse({
                "error_message": "This email already exists!",
                "error_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
            serializer.save()
            return JsonResponse({
                "message": "Register successful!"
            }, status=status.HTTP_201_CREATED)
        
        return JsonResponse({
            "error_message": "Invalid data!",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, customer_id):
        """Update an existing customer by ID (Authentication Required)"""
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)  # Allows partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id):
        """Delete a customer by ID (Authentication Required)"""
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DebugAuthView(APIView):
    def get(self, request):
        auth_header = request.headers.get("Authorization", "No Auth Header Found")
        return Response({"Received Authorization Header": auth_header})