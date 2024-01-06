from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from encryption import views


router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Encryption API",
      default_version='v1',
      description="Encryption API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mikhailvolvach@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path(r'api/data', views.DataList.as_view(), name='data-list'),

    path(r'api/data/<int:id>', views.DataListItem.as_view(), name='data-item'),
    path(r'api/data/<int:id>/add-to-request/', views.add_data_to_request, name='add-data-item-to-request'),

    path(r'api/data/<int:id>/delete-from-request/', views.delete_data_from_encryption_req, name='delete-data-item-from-request'),

    path(r'api/encryption-requests/', views.get_encryption_reqs , name='get-encryption-requests'),
    path(r'api/encryption-requests/<int:id>', views.DataEncryptionReqItem.as_view(), name='encryption-request'),
    
    path(r'api/encryption-requests/form/', views.form_encryption_req, name='form-encryption-request'),
    path(r'api/encryption-requests/<int:id>/change-status/', views.change_encryption_req_status, name='change-encryption-request-status'),
   path(r'api/login', views.login_view, name='login'),
    path(r'api/logout', views.logout_view, name='logout'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    

    # path('/user')
]
