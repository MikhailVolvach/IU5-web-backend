from app.models.encription_request import Encription_Request
from app.models.encription_service import Encription_Service
from app.config.types import Request_Type


services_collection = [
    Encription_Service("bi bi-credit-card", "Зашифровать карту", "Шифрование данных банковской карты", 1000),
    Encription_Service("bi bi-envelope", "Зашифровать почту", "Шифрование электронной почты", 2000),
    Encription_Service("bi bi-file-earmark", "Зашифровать файл", "Шифрование файлов", 3000),
    Encription_Service("bi bi-file-earmark", "Зашифровать пароль", "Шифрование пароля", 4000),
]

requests_collection = [
    Encription_Request(Request_Type.ENCRIPTION, services_collection[0]),
    Encription_Request(Request_Type.DECRIPTION, services_collection[0]),
    Encription_Request(Request_Type.ENCRIPTION, services_collection[1]),
    Encription_Request(Request_Type.DECRIPTION, services_collection[1]),
    Encription_Request(Request_Type.ENCRIPTION, services_collection[2]),
    Encription_Request(Request_Type.DECRIPTION, services_collection[2]),
]

