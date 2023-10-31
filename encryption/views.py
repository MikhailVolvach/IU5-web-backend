from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest
from .serializers import DataItemSerializer, DataEncriptionRequestSerializer
from datetime import datetime


######
# Data
######

@api_view(['Get'])
def get_data_list(request, format=None):
    query = request.GET.get('data_search')

    if not query: query = ""

    data_list = DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')
    serializer = DataItemSerializer(data_list, many=True)

    
    try:
        req_id = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT).id
    except:
        req_id = None    

    return Response({
        # В будущем добавить прорверку на пользователя
        "request_id": req_id,
        "data": serializer.data})


@api_view(['POST'])
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


@api_view(['Delete'])
def delete_data_item(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    # data_item.is_deleted = True
    serializer = DataItemSerializer(data_item, data={"is_deleted": True}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def add_data_to_request(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)

    # Попытка взять заявку, в противном случае создать заявку
    try:
        # ДОРАБОТАТЬ:
        # Добавить в get уточнение пользователя
        # Добавление данных в последнюю заявку со статусом черновик
        encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT)
        
        # encryption = DataEncryptionRequest.objects.get(id=request.data["request_id"])
    except:
        encryption = DataEncryptionRequest.objects.create(work_status=DataEncryptionRequest.Status.DRAFT,
                                                          creation_date=timezone.now(),
                                                          formation_date=timezone.now(),
                                                          user_id=1)

    # Добавление в М-М таблицу записи с текущей заявкой и услугой
    data_item.dataencryptionrequest_set.add(encryption)
    
    return Response({
        "request": DataEncriptionRequestSerializer(encryption).data,
        "data": DataItemSerializer(encryption.data_item.all(), many=True).data
    })


####################
# EncryptionRequests
####################

@api_view(['Get'])
def get_encryption_reqs(request, format=None):
    requests = DataEncryptionRequest.objects.all().order_by(*request.GET.get("order_by").split(','))

    serializer = DataEncriptionRequestSerializer(requests, many=True)

    return Response(serializer.data)


@api_view(['Get'])
def get_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    encryption_serializer = DataEncriptionRequestSerializer(encryption_req)
    data_items_serializer = DataItemSerializer(encryption_req.data_item.all(), many=True)

    return Response({
        'request': encryption_serializer.data,
        'owner': encryption_req.user.username,
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


@api_view(['Delete'])
def delete_encryption_req(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    
    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.DELETED}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_data_from_encryption_req(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)

    try:
        data_item.dataencryptionrequest_set.remove(get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response()


# Сформировать можем только черновик (черновик может быть всего 1 у пользователя)
@api_view(['Put'])
def form_encryption_req(request, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT)

    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.FORMED, "formation_date": timezone.now}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# Только для сформированных заявок
@api_view(['Put'])
def change_encryption_req_status(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
    
    # Сформированную заявку можно только завершить, отменить или удалить
    if encryption_req.work_status == DataEncryptionRequest.Status.FORMED:
        if request.data["work_status"] not in [DataEncryptionRequest.Status.DELETED, DataEncryptionRequest.Status.FINALISED, DataEncryptionRequest.Status.CANCELLED]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": request.data["work_status"], "formation_date": timezone.now}, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
