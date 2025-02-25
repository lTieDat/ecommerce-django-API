import json
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
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class CustomerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, username=None):
        """Retrieve all customers or a specific customer by ID (Authentication Required)"""
        if username:
            customer = get_object_or_404(Customer, email=username)
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

@csrf_exempt
def custom_login_page(request):
    if request.method == 'POST':
        # Parse the JSON body
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(username)  
            print(password) 

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Generate tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            tokens = str(refresh.access_token),    
            customer = Customer.objects.get(email=username)
            # serialize the customer object
            customer = CustomerSerializer(customer).data
            
            response = JsonResponse({'message': 'Login successful' ,'tokens': tokens, 'user': customer})

            return response
        else:
            # Return 401 Unauthorized for invalid credentials
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # Render the login page for GET requests
    else:
        return render(request, 'login.html')

@csrf_exempt
def customer_register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the email already exists
        if Customer.objects.filter(email=email).exists():
            return JsonResponse({
                "error_message": "This email already exists!",
                "error_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create a new customer
        new_customer = Customer.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )
        new_customer.save()

        return JsonResponse({
            "message": "Register successful!"
        }, status=status.HTTP_201_CREATED)

    # Render the register page for GET requests
    return render(request, 'register.html')
