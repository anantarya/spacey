# in views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Employee
from ..serializers import EmployeeSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
def employee_register(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
