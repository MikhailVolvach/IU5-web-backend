from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest
from .serializers import DataItemSerializer, DataEncriptionRequestSerializer


######
# Data
######

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
    data_item.set_is_deleted()
    serializer = DataItemSerializer(data_item)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def add_data_to_request(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)

    # Попытка взять заявку, в противном случае создать заявку
    try:
        encryption = DataEncryptionRequest.objects.get(id=request.data["request_id"])
    except:
        encryption = DataEncryptionRequest.objects.create(work_status=DataEncryptionRequest.Status.INTRODUCED,
                                                          creation_date=timezone.now(),
                                                          formation_date=timezone.now(),
                                                          user_id=1)

    # Добавление в М-М таблицу записи с текущей заявкой и услугой
    data_item.dataencryptionrequest_set.add(encryption)

    return Response()


####################
# EncryptionRequests
####################

@api_view(['Get'])
def get_encryption_requests(request, format=None):
    requests = DataEncryptionRequest.objects.all()
    serializer = DataEncriptionRequestSerializer(requests, many=True)

    return Response(serializer.data)


@api_view(['Get'])
def get_encryption_request(request, id, format=None):
    encryption_request = get_object_or_404(DataEncryptionRequest, id=id)
    encryption_serializer = DataEncriptionRequestSerializer(encryption_request)
    data_items_serializer = DataItemSerializer(encryption_request.data_item.all(), many=True)

    print(data_items_serializer.data)

    return Response({
        'request': encryption_serializer.data,
        'data': data_items_serializer.data
    })


@api_view(['Put'])
def change_encryption_request(request, id, format=None):
    encryption_request = get_object_or_404(DataItem, id=id)
    serializer = DataEncriptionRequestSerializer(encryption_request, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Put'])
def delete_encryption_request(request, id, format=None):
    encryption_request = get_object_or_404(DataItem, id=id)
    encryption_request.set_is_deleted()
    serializer = DataEncriptionRequestSerializer(encryption_request)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)