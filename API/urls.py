from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from encryption import views


router = routers.DefaultRouter()


urlpatterns = [
path('', include(router.urls)),
    path(r'data/', views.get_data_list, name='get-data'),
    path(r'data/post/', views.post_data_item, name='post-data'),
    path(r'data/<int:id>/', views.get_data_item, name='get-data-item'),
    path(r'data/<int:id>/put/', views.change_data_item, name='put-data-item'),
    path(r'data/<int:id>/delete/', views.delete_data_item, name='delete-data-item'),
    path(r'data/<int:id>/add-to-request/', views.add_data_to_request, name='add-data-item-to-request'),

    path(r'data/<int:id>/delete-from-request/', views.delete_data_from_encryption_req, name='delete-data-item-from-request'),

    path(r'encryption_requests/', views.get_encryption_reqs , name='get-encryption-requests'),
    path(r'encryption_requests/<int:id>/', views.get_encryption_req, name='get-encryption-request'),
    path(r'encryption_requests/<int:id>/put/', views.change_encryption_req, name='put-encryption-request'),
    path(r'encryption_requests/<int:id>/delete/', views.delete_encryption_req, name='delete-encryption-request'),
    path(r'encryption_requests/form/', views.form_encryption_req, name='form-encryption-request'),
    path(r'encryption_requests/<int:id>/change_status/', views.change_encryption_req_status, name='change-encryption-request-status'),

    # path(r'encryption_requests/<int:id>/delete-data-item', views.delete_data_from_encryption_req, name='delete-data-from-request'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]
