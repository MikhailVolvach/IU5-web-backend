from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest
from .serializers import DataItemSerializer, DataEncriptionRequestSerializer
from datetime import datetime
from django.conf import settings

class DataList(APIView):
    data_item_model_class = DataItem
    data_req_model_class = DataEncryptionRequest
    data_item_serializer = DataItemSerializer

    def get(self, request, format=None):
        query = request.GET.get('data_search')

        if not query: query = ""

        data_list = self.data_item_model_class.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')
        serializer = self.data_item_serializer(data_list, many=True)

        try:
            req_id = self.data_req_model_class.objects.get(work_status=self.data_req_model_class.Status.DRAFT).id
        except:
            req_id = None

        return Response({
            #TODO: В будущем добавить прорверку на пользователя
            "request_id": req_id,
            "data": serializer.data})

    @swagger_auto_schema(request_body=data_item_serializer)
    def post(self, request, format=None):
        serializer = self.data_item_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataListItem(APIView):
    data_item_serializer = DataItemSerializer
    data_item_model = DataItem

    def get(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)

        serializer = self.data_item_serializer(data_item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=data_item_serializer)
    def put(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data={"is_deleted": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataEncryptionReqItem(APIView):
    data_encryption_req_model = DataEncryptionRequest
    data_encryption_req_serializer = DataEncriptionRequestSerializer
    data_item_serializer = DataItemSerializer

    def get(self, request, id, format=None):
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)
        encryption_serializer = self.data_encryption_req_serializer(encryption_req)
        data_items_serializer = self.data_item_serializer(encryption_req.data_item.all(), many=True)

        return Response({
            'request': encryption_serializer.data,
            'owner': encryption_req.user.username,
            'data': data_items_serializer.data
        })


    @swagger_auto_schema(request_body=data_encryption_req_serializer)
    def put(self, request, id, format=None):
        # TODO: Добавить проверку изменения статуса заявки
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)
        serializer = self.data_encryption_req_serializer(encryption_req, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("Ошибка изменения заявки", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)

        serializer = self.data_encryption_req_serializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.DELETED}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("Ошибка удаления заявки", status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
def add_data_to_request(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    # Попытка взять заявку, в противном случае создать заявку
    try:
        # Добавление данных в последнюю заявку со статусом черновик
        encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT)
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

@api_view(['Get'])
def get_encryption_reqs(request, format=None):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_date = timezone.datetime.min

    if end_date:
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d") + timezone.timedelta(days=1)
    else:
        end_date = timezone.datetime.max

    requests = DataEncryptionRequest.objects.filter(creation_date__gte=start_date, creation_date__lt=end_date)

    serializer = DataEncriptionRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['Delete'])
def delete_data_from_encryption_req(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    try:
        data_item.dataencryptionrequest_set.remove(get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response()

# Только для сформированных заявок
@swagger_auto_schema(request_body=DataEncriptionRequestSerializer, method='put')
@api_view(['Put'])
def change_encryption_req_status(request, id, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, id=id)

    # Сформированную заявку можно только завершить, отменить или удалить
    if encryption_req.work_status == DataEncryptionRequest.Status.FORMED:
        if request.data["work_status"] not in [DataEncryptionRequest.Status.DELETED,
                                               DataEncryptionRequest.Status.FINALISED,
                                               DataEncryptionRequest.Status.CANCELLED]:
            return Response(data="Сформированную заявку можно только удалить, завершить или отменить",
                            status=status.HTTP_400_BAD_REQUEST)  # Отобразить текст ошибки
    else:
        return Response(data='Текущая заявка не находится в статусе Сформирован', status=status.HTTP_400_BAD_REQUEST)

    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": request.data["work_status"],
                                                                       "formation_date": timezone.now()}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response("Ошибка изменения статуса заявки", status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(request_body=DataEncriptionRequestSerializer, method='put')
@api_view(['Put'])
def form_encryption_req(request, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT, user=request.user)

    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.FORMED, "formation_date": timezone.now()}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response("Ошибка формирования заявки", status=status.HTTP_400_BAD_REQUEST)
