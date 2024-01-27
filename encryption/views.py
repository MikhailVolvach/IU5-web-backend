from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DataItem, DataEncryptionRequest, EncryptionUser
from .serializers import DataItemSerializer, DataEncryptionRequestSerializer, EncryptionUserSerializer
from datetime import datetime
from encryption.permissions import IsModerator, IsAdmin, IsUser
from django.conf import settings
import redis
import uuid
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = EncryptionUser.objects.all()
    serializer_class = EncryptionUserSerializer
    model_class = EncryptionUser

    def list(self, request):
        ssid = request.session.get('session_id')

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user is None or ssid_user.role != EncryptionUser.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(self.serializer_class(self.queryset, many=True).data, status=status.HTTP_200_OK)

    def create(self, request):
        if self.model_class.objects.filter(username=request.data['username']).exists():
            return Response({'status': 'Exists'}, status=400)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.data['role'] == EncryptionUser.Roles.ADMIN:
                self.model_class.objects.create_superuser(
                    username=serializer.data['username'],
                    password=serializer.data['password'],
                    role=serializer.data['role']
                )
            elif serializer.data['role'] == EncryptionUser.Roles.MODERATOR:
                self.model_class.objects.create_moderator(
                    username=serializer.data['username'],
                    password=serializer.data['password'],
                    role=serializer.data['role']
                )
            else:
                self.model_class.objects.create_user(
                    username=serializer.data['username'],
                    password=serializer.data['password'],
                    role=serializer.data['role']
                )

            return Response({'status': 'Success'}, status=200)

        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post', 
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, desription='Имя пользователя'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, desription='Пароль пользователя')
        },
        required=['username', 'password']
    ),
    operation_description='Метод авторизации'
)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request, format=None):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    print(user, username, password, authenticate(request, username='mikhail', password='1234'))
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        session_storage.expire(random_key, 86400)

        user_serializer = EncryptionUserSerializer(user)

        request.session['session_id'] = random_key

        try:
            order_id = get_object_or_404(DataEncryptionRequest, user=user, work_status=DataEncryptionRequest.Status.DRAFT).id
        except:
            order_id = None

        response = JsonResponse({
            'user': user_serializer.data, 
            'order_id': order_id})
        
        response.set_cookie('session_id', random_key)

        return response
    else:
        return JsonResponse({'status': 'error', 'error': 'login failed'})

   
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
def logout_view(request, format=None):
    ssid = request.session.get('session_id')

    if ssid:
        # Удаляем данные сессии из Redis
        session_storage.delete(ssid)

    # Выход пользователя
    logout(request)
    
    return JsonResponse({'status': 'ok'})

@api_view(['Get'])
@authentication_classes([SessionAuthentication])
def get_auth_user(request, format=None):
    ssid = request.session.get('session_id')
    
    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    try:
        order_id = get_object_or_404(DataEncryptionRequest, user=ssid_user, work_status=DataEncryptionRequest.Status.DRAFT).id
    except:
        order_id = None

    return JsonResponse({'user': EncryptionUserSerializer(ssid_user).data,
                         'order_id': order_id})


class DataList(APIView):
    data_item_model_class = DataItem
    data_req_model_class = DataEncryptionRequest
    data_item_serializer = DataItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['search']
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        query = request.GET.get('search')

        if not query: query = ""

        data_list = self.data_item_model_class.objects.filter(is_deleted=False).filter(title__icontains=query).order_by(
            'id')
        serializer = self.data_item_serializer(data_list, many=True)

        try:
            ssid = request.COOKIES['session_id']
            session_storage.get(ssid)
            ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))
            req_id = self.data_req_model_class.objects.get(work_status=self.data_req_model_class.Status.DRAFT, user=ssid_user).id
        except:
            req_id = None

        return Response({
            # TODO: В будущем добавить прорверку на пользователя
            "request_id": req_id,
            "data": serializer.data})

    @swagger_auto_schema(request_body=data_item_serializer)
    def post(self, request, format=None):
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user.role != EncryptionUser.Roles.MODERATOR or not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.data_item_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataListItem(APIView):
    data_item_serializer = DataItemSerializer
    data_item_model = DataItem
    authentication_classes = [SessionAuthentication]

    def get(self, request, id, format=None):
        data_item = get_object_or_404(self.data_item_model, id=id)

        serializer = self.data_item_serializer(data_item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=data_item_serializer)
    def put(self, request, id, format=None):
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user.role not in [EncryptionUser.Roles.ADMIN, EncryptionUser.Roles.MODERATOR] or not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user.role not in [EncryptionUser.Roles.ADMIN,
                                  EncryptionUser.Roles.MODERATOR] or not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data_item = get_object_or_404(self.data_item_model, id=id)
        serializer = self.data_item_serializer(data_item, data={"is_deleted": True}, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataEncryptionReqItem(APIView):
    data_encryption_req_model = DataEncryptionRequest
    data_encryption_req_serializer = DataEncryptionRequestSerializer
    data_item_serializer = DataItemSerializer
    authentication_classes = [SessionAuthentication]

    def get(self, request, id, format=None):
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id, user=ssid_user)
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
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user.role not in [EncryptionUser.Roles.ADMIN,
                                  EncryptionUser.Roles.MODERATOR] or not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)
        serializer = self.data_encryption_req_serializer(encryption_req, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response("Ошибка изменения заявки", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        ssid = request.session.get('session_id')

        if not ssid:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        if ssid_user.role not in [EncryptionUser.Roles.ADMIN,
                                  EncryptionUser.Roles.MODERATOR] or not ssid_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        encryption_req = get_object_or_404(self.data_encryption_req_model, id=id)

        serializer = self.data_encryption_req_serializer(encryption_req,
                                                         data={"work_status": DataEncryptionRequest.Status.DELETED},
                                                         partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response("Ошибка удаления заявки", status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
@authentication_classes([SessionAuthentication])
def add_data_to_request(request, id, format=None):
    ssid = request.session.get('session_id')

    if not ssid:
        return Response(status=status.HTTP_403_FORBIDDEN)

    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    if ssid_user.role != EncryptionUser.Roles.USER or not ssid_user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    data_item = get_object_or_404(DataItem, id=id)
    # Попытка взять заявку, в противном случае создать заявку
    try:
        # Добавление данных в последнюю заявку со статусом черновик
        encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT,
                                                       user=ssid_user.id)
    except:
        encryption = DataEncryptionRequest.objects.create(work_status=DataEncryptionRequest.Status.DRAFT,
                                                          creation_date=timezone.now(),
                                                          formation_date=timezone.now(),
                                                          user_id=ssid_user.id)

    # Добавление в М-М таблицу записи с текущей заявкой и услугой
    data_item.dataencryptionrequest_set.add(encryption)
    return Response({
        "request": DataEncryptionRequestSerializer(encryption).data,
        "data": DataItemSerializer(encryption.data_item.all(), many=True).data
    })


@api_view(['Get'])
@authentication_classes([SessionAuthentication])
def get_encryption_reqs(request, format=None):
    ssid = request.session.get('session_id')

    if not ssid:
        return Response(status=status.HTTP_403_FORBIDDEN)

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

    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    if not ssid_user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if ssid_user.is_staff:
        requests = DataEncryptionRequest.objects.filter(creation_date__gte=start_date, creation_date__lt=end_date)
    else:
        requests = DataEncryptionRequest.objects.filter(creation_date__gte=start_date, creation_date__lt=end_date,
                                                        user=ssid_user.id)

    serializer = DataEncryptionRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['Delete'])
@authentication_classes([SessionAuthentication])
def delete_data_from_encryption_req(request, id, format=None):
    ssid = request.session.get('session_id')

    if not ssid:
        return Response(status=status.HTTP_403_FORBIDDEN)

    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    if ssid_user.role != EncryptionUser.Roles.USER or not ssid_user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    data_item = get_object_or_404(DataItem, id=id)
    try:
        data_item.dataencryptionrequest_set.remove(
            get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT,
                              user=ssid_user.id))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    encryption = DataEncryptionRequest.objects.get(work_status=DataEncryptionRequest.Status.DRAFT,
                                                       user=ssid_user.id)

    return Response({
        "request": DataEncryptionRequestSerializer(encryption).data,
        "data": DataItemSerializer(encryption.data_item.all(), many=True).data
    })


# Только для сформированных заявок
# @swagger_auto_schema(request_body=DataEncryptionRequestSerializer, method='put')
@swagger_auto_schema(
    method='Put', 
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, desription='Статус заявки'),
        },
        required=['status']
    ),
    operation_description='Метод изменения статуса заявки'
)
@api_view(['Put'])
@authentication_classes([SessionAuthentication])
def change_encryption_req_status(request, id, format=None):
    ssid = request.session.get('session_id')

    if not ssid:
        return Response(status=status.HTTP_403_FORBIDDEN)

    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    if ssid_user.role != EncryptionUser.Roles.MODERATOR or not ssid_user:
        return Response(status=status.HTTP_403_FORBIDDEN)

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

    serializer = DataEncryptionRequestSerializer(encryption_req, data={"work_status": request.data["work_status"],
                                                                       "formation_date": timezone.now()}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response("Ошибка изменения статуса заявки", status=status.HTTP_400_BAD_REQUEST)


# Сформировать можем только черновик (черновик может быть всего 1 у пользователя) (делает это пользователь)
# @swagger_auto_schema(method='Put')
@api_view(['Put'])
@authentication_classes([SessionAuthentication])
def form_encryption_req(request, format=None):
    ssid = request.session.get('session_id')

    print(ssid)

    if not ssid:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    ssid_user = EncryptionUser.objects.get(username=session_storage.get(ssid).decode('utf-8'))

    if ssid_user.role != EncryptionUser.Roles.USER or not ssid_user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    encryption_req = get_object_or_404(DataEncryptionRequest, work_status=DataEncryptionRequest.Status.DRAFT,
                                       user=ssid_user)

    serializer = DataEncryptionRequestSerializer(encryption_req,
                                                 data={"work_status": DataEncryptionRequest.Status.FORMED,
                                                       "formation_date": timezone.now()}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response("Ошибка формирования заявки", status=status.HTTP_400_BAD_REQUEST)
