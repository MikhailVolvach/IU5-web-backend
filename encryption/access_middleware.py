# from django.http import HttpResponseForbidden
# from .views import session_storage
# from django.urls import resolve
#
# class AccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         req_permissions = self.get_required_permissions(request)
#         # print(req_permissions)
#         if not req_permissions:
#             return self.get_response(request)
#
#         print(self.check_permission(request, req_permissions))
#         # if (req_permissions)
#
#         ssid = request.COOKIES.get('session_id')
#         return self.get_response(request)
#         # print(req_permission)
#
#         # if ssid:
#         #     try:
#         #         session_storage.get(ssid)
#         #
#         #     except:
#         #         pass
#
#
#
#     def check_permission(self, request, permissions):
#         is_permitted = False
#         # for permission in permissions:
#             # if permission.has_permission(request):
#             #     is_permitted = True
#             #     break
#         return is_permitted
#
#     def get_required_permissions(self, request):
#         # Извлекаем разрешения из декораторов permission_classes представления
#         try:
#             # Получаем представление для текущего запроса
#             view_func = resolve(request.path_info).func
#             # print(view_func)
#             # Ищем атрибут required_permissions, который был добавлен через декоратор @permission_classes
#             attr = getattr(view_func, 'permission_classes')
#             # print(attr)
#             return attr
#         except Exception as e:
#             print(e)
#             return []
