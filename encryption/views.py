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
def get_encryption_reqs(request, format=None):
    requests = DataEncryptionRequest.objects.all()
    serializer = DataEncriptionRequestSerializer(requests, many=True)

    return Response(serializer.data)


@api_view(['Get'])
def get_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    encryption_serializer = DataEncriptionRequestSerializer(encryption_req)
    data_items_serializer = DataItemSerializer(encryption_req.data_item.all(), many=True)

    print(data_items_serializer.data)

    return Response({
        'request': encryption_serializer.data,
        'data': data_items_serializer.data
    })


@api_view(['Put'])
def change_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    serializer = DataEncriptionRequestSerializer(encryption_req, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Put'])
def delete_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    encryption_req.set_is_deleted()
    serializer = DataEncriptionRequestSerializer(encryption_req)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def delete_data_from_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)

    try:
        encryption_req.data_item.get(id=request.data['data_item_id']).dataencryptionrequest_set.remove(encryption_req)
        # data_item = get_object_or_404(DataItem, id=request.data['data_item_id'])
        # data_item.dataencryptionrequest_set.remove(encryption_req)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'request': DataEncriptionRequestSerializer(encryption_req).data,
        'data': DataItemSerializer(encryption_req.data_item.all(), many=True).data
    })
