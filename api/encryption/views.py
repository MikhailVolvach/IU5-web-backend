from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest
from .serializers import DataItemSerializer, DataEncriptionRequestSerializer

# Data
@api_view(['Get'])
def get_data_list(request, format=None):
    query = request.GET.get('data_search')
    
    if not query: query = ""
    
    data_list = DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')
    serializer = DataItemSerializer(data_list, many=True)
    
    return Response(serializer.data)


@api_view(['Post'])
def post_data_item(request, format=None):
    serializer = DataItemSerializer(data=request.data)
     
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get'])
def get_data_item(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    if request.method == 'GET':
        serializer = DataItemSerializer(data_item)
        return Response(serializer.data)


@api_view(['Put'])
def change_data_item(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    serializer = DataItemSerializer(data_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Put'])
def delete_data_item(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    DataItem.set_is_deleted()
    serializer = DataItemSerializer(data_item)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# EncryptionRequests

@api_view(['Get'])
def get_encryption_requests(request, format=None):
    requests = DataEncryptionRequest.objects.all()
    serializer = DataEncriptionRequestSerializer(requests, many=True)

    return Response(serializer.data)


@api_view(['Get'])
def get_encryption_request(request, id, format=None):
    request = get_object_or_404(DataEncryptionRequest, id=id)

    if request.method == 'GET':
        serializer = DataEncriptionRequestSerializer(request)
        return Response(serializer.data)


@api_view(['Post'])
def post_encryption_request(request, format=None):
    serializer = DataEncriptionRequestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




