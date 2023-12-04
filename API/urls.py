from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from encryption import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'data/', views.DataList.as_view(), name='data-list'),

    path(r'data/<int:id>/', views.DataListItem.as_view(), name='data-item'),
    path(r'data/<int:id>/add-to-request/', views.add_data_to_request, name='add-data-item-to-request'),

    path(r'data/<int:id>/delete-from-request/', views.delete_data_from_encryption_req, name='delete-data-item-from-request'),

    path(r'encryption-requests/', views.get_encryption_reqs , name='get-encryption-requests'),
    path(r'encryption-requests/<int:id>/', views.DataEncryptionReqItem.as_view(), name='encryption-request'),
    
    path(r'encryption-requests/form/', views.form_encryption_req, name='form-encryption-request'),
    path(r'encryption-requests/<int:id>/change-status/', views.change_encryption_req_status, name='change-encryption-request-status'),

    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
