# views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..models import Product
from ..serializers import ProductSerializer
from django.db import connection
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


'''@api_view(['POST'])
def employee_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    '''
@csrf_exempt  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])

def product_add( request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            product_name = serializer.validated_data['product_name']
            quantity = serializer.validated_data['quantity']
            unit_price = serializer.validated_data['unit_price']
            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Products (product_name, quantity, unit_price) VALUES(%s,%s, %s)", [product_name, quantity, unit_price])
            return JsonResponse(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def product(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM "Products"')
            columns = [col[0] for col in cursor.description]
            products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return JsonResponse({'products': products})
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def product_update(request, id):
    if request.method == 'PUT':
        try:
            # Retrieve the existing product instance
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Deserialize the request data using the serializer
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract data from the serializer
            product_name = serializer.validated_data.get('product_name', product.product_name)
            quantity = serializer.validated_data.get('quantity', product.quantity)
            unit_price = serializer.validated_data.get('unit_price', product.unit_price)
            
            # Execute raw SQL query to update the product in the database
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Products SET product_name=%s, quantity=%s, unit_price=%s WHERE id=%s", [product_name, quantity, unit_price, id])
                
            return JsonResponse({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)            
            
        
@csrf_exempt        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def product_delete(request, id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
