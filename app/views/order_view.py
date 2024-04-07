from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ..models import Customer, Product, Order
from ..serializers import OrderSerializer
from rest_framework.response import Response
from decimal import Decimal

@api_view(['POST'])
def bill_customer(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    # Convert string inputs to integers
    try:
        customer_id = int(customer_id)
        product_id = int(product_id)
        quantity = int(quantity)
    except ValueError:
        return JsonResponse({'error': 'Invalid input data'}, status=400)

    # Retrieve customer and product objects
    customer = get_object_or_404(Customer, pk=customer_id)
    product = get_object_or_404(Product, pk=product_id)

    # Check if product quantity is sufficient
    if int(product.quantity) > int(quantity):
        return JsonResponse({'error': 'Insufficient product quantity'}, status=400)

    # Calculate total amount based on product price and quantity
    try:
        total_amount = Decimal(product.unit_price) * Decimal(quantity)
    except TypeError:
        return JsonResponse({'error': 'Invalid product price'}, status=400)

    # Create order record
    order = Order.objects.create(
        customer=customer,
        product=product,
        quantity=quantity,
        total_amount=total_amount,
        payment_method='Cash'
    )

    # Update product quantity
    product.quantity = int(product.quantity) - int(quantity)
    product.save()

    return JsonResponse({'message': 'Order placed successfully'}, status=201)


@api_view(['GET'])
def get_past_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)