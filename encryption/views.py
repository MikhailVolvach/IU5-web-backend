from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest, EncryptionUser
from .serializers import DataItemSerializer, DataEncriptionRequestSerializer, EncryptionUserSerializer
from datetime import datetime
from encryption.permissions import IsModerator, IsAdmin, IsUser
from django.conf import settings
import redis
import uuid

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = EncryptionUser.objects.all()
    serializer_class = EncryptionUserSerializer
    model_class = EncryptionUser

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdmin | IsModerator]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request):
        print(request)
        if self.model_class.objects.filter(username=request.data['username']).exists():
            return Response({'status': 'Exists'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(username=serializer.data['username'],
                                                 password=serializer.data['password'],
                                                 role=serializer.data['role'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


@permission_classes([AllowAny])
@csrf_exempt
@swagger_auto_schema(method='post', request_body=EncryptionUserSerializer)
@api_view(['Post'])
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    # print(username)
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        random_key = uuid.uuid4()
        session_storage.set(random_key, username)

        response = HttpResponse("{'status': 'ok'}")
        response.set_cookie("session_id", random_key)
        # print(response)

        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

def logout_view(request):
    logout(request._request)
    return Response("{'status': 'Success'}")

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
    @method_permission_classes((IsAdmin,IsModerator))
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
    @method_permission_classes((IsAdmin,IsModerator))
    def put(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAdmin,IsModerator))
    def delete(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data={"is_deleted": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataEncryptionReqItem(APIView):
    permission_classes = [IsAuthenticated]
    data_encryption_req_model = DataEncryptionRequest
    data_encryption_req_serializer = DataEncriptionRequestSerializer
    data_item_serializer = DataItemSerializer

    def get(self, request, id, format=None):
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id, user=request.user.id)
        encryption_serializer = self.data_encryption_req_serializer(encryption_req)
        data_items_serializer = self.data_item_serializer(encryption_req.data_item.all(), many=True)

        return Response({
            'request': encryption_serializer.data,
            'owner': encryption_req.user.username,
            'data': data_items_serializer.data
        })


    @swagger_auto_schema(request_body=data_encryption_req_serializer)
    @method_permission_classes((IsModerator, IsAdmin))
    def put(self, request, id, format=None):
        # TODO: Добавить проверку изменения статуса заявки
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)
        serializer = self.data_encryption_req_serializer(encryption_req, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("Ошибка изменения заявки", status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsModerator, IsAdmin))
    def delete(self, request, id, format=None):
        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)

        serializer = self.data_encryption_req_serializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.DELETED}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("Ошибка удаления заявки", status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def data(request, format=None):
#     if request.method == 'GET':
#         # get_data_list(request)
#         query = request.GET.get('data_search')
#
#         if not query: query = ""
#
#         data_list = DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')
#         serializer = DataItemSerializer(data_list, many=True, context={'request': request})
#
#         try:
#             req_id = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT).id
#         except:
#             req_id = None
#
#         return Response({
#             # В будущем добавить прорверку на пользователя
#             "request_id": req_id,
#             "data": serializer.data})
#     elif request.method == 'POST':
#         serializer = DataItemSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'PUT', 'DELETE'])
# def data_item(request, id, format=None):
#     if request.method == 'GET':
#         data_item = get_object_or_404(DataItem, id=id)
#         serializer = DataItemSerializer(data_item)
#
#         # data = serializer.data
#         #
#         # # Изменяем значение поля img
#         # if 'img' in data and data['img']:
#         #     # Заменяем "http://nginx:9000" на "http://localhost:9000"
#         #     data['img'] = data['img'].replace("http://nginx:9000", "http://localhost:9000")
#
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         data_item = get_object_or_404(DataItem, id=id)
#         serializer = DataItemSerializer(data_item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         data_item = get_object_or_404(DataItem, id=id)
#         serializer = DataItemSerializer(data_item, data={"is_deleted": True}, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsUser])
@authentication_classes([IsUser])
@api_view(['Post'])
def add_data_to_request(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    # print(request.user)
    # Попытка взять заявку, в противном случае создать заявку
    try:
        # Добавление данных в последнюю заявку со статусом черновик
        encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT, user=request.user.id)
        # encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT)
    except:
        encryption = DataEncryptionRequest.objects.create(work_status=DataEncryptionRequest.Status.DRAFT,
                                                          creation_date=timezone.now(),
                                                          formation_date=timezone.now(),
                                                          user_id=request.user.id)
        # encryption = DataEncryptionRequest.objects.create(work_status=DataEncryptionRequest.Status.DRAFT,
        #                                                   creation_date=timezone.now(),
        #                                                   formation_date=timezone.now())

    # Добавление в М-М таблицу записи с текущей заявкой и услугой
    data_item.dataencryptionrequest_set.add(encryption)
    
    return Response({
        "request": DataEncriptionRequestSerializer(encryption).data,
        "data": DataItemSerializer(encryption.data_item.all(), many=True).data
    })

@permission_classes([IsAuthenticated])
@authentication_classes([])
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

    requests = DataEncryptionRequest.objects.filter(creation_date__gte=start_date, creation_date__lt=end_date, user=request.user.id)

    serializer = DataEncriptionRequestSerializer(requests, many=True)
    return Response(serializer.data)

@permission_classes([IsUser])
@authentication_classes([])
@api_view(['Delete'])
def delete_data_from_encryption_req(request, id, format=None):
    data_item = get_object_or_404(DataItem, id=id)
    try:
        data_item.dataencryptionrequest_set.remove(get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT, user=request.user.id))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response()


# Только для сформированных заявок
@permission_classes([IsModerator])
@authentication_classes([IsModerator])
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

# Сформировать можем только черновик (черновик может быть всего 1 у пользователя)
@permission_classes([IsAuthenticated])
@authentication_classes([])
@swagger_auto_schema(request_body=DataEncriptionRequestSerializer, method='put')
@api_view(['Put'])
def form_encryption_req(request, format=None):
    encryption_req = get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT, user=request.user)

    serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.FORMED, "formation_date": timezone.now()}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response("Ошибка формирования заявки", status=status.HTTP_400_BAD_REQUEST)

# @api_view(['Get'])
# def get_encryption_req(request, id, format=None):
#     encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#     encryption_serializer = DataEncriptionRequestSerializer(encryption_req)
#     data_items_serializer = DataItemSerializer(encryption_req.data_item.all(), many=True)
#
#     return Response({
#         'request': encryption_serializer.data,
#         'owner': encryption_req.user.username,
#         'data': data_items_serializer.data
#     })


# @api_view(['Put'])
# def change_encryption_req(request, id, format=None):
#     encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#     serializer = DataEncriptionRequestSerializer(encryption_req, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['Delete'])
# def delete_encryption_req(request, id, format=None):
#     encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#
#     serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.DELETED}, partial=True)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def encryption_req(request, id, format=None):
#     if request.method == 'GET':
#             encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#             encryption_serializer = DataEncriptionRequestSerializer(encryption_req)
#             data_items_serializer = DataItemSerializer(encryption_req.data_item.all(), many=True)
#
#             return Response({
#                 'request': encryption_serializer.data,
#                 'owner': encryption_req.user.username,
#                 'data': data_items_serializer.data
#             })
#     elif request.method == 'PUT':
#         encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#         serializer = DataEncriptionRequestSerializer(encryption_req, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response("Ошибка изменения заявки", status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         encryption_req = get_object_or_404(DataEncryptionRequest, id=id)
#
#         serializer = DataEncriptionRequestSerializer(encryption_req, data={"work_status": DataEncryptionRequest.Status.DELETED}, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response("Ошибка удаления заявки", status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)


