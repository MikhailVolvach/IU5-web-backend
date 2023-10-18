from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from encryption import views


router = routers.DefaultRouter()


urlpatterns = [
path('', include(router.urls)),
    path(r'data/', views.get_data_list, name='data-list'),
    path(r'data/post/', views.post_data_item, name='post-data'),
    path(r'data/<int:id>/', views.get_data_item, name='data-item'),
    path(r'data/<int:id>/put/', views.change_data_item, name='put-data'),
    path(r'data/<int:id>/delete/', views.delete_data_item, name='delete-data'),
    path(r'data/<int:id>/add_to_request/', views.add_data_to_request, name='add-data-to-request'),

    path(r'encryption_requests/', views.get_encryption_reqs , name='encryption-requests-list'),
    path(r'encryption_requests/<int:id>/', views.get_encryption_req, name='encryption-request-item'),
    path(r'encryption_requests/<int:id>/put', views.change_encryption_req, name='put-encryption-request'),
    path(r'encryption_requests/<int:id>/delete', views.delete_encryption_req, name='delete-encryption-request'),
    path(r'encryption_requests/<int:id>/approve', views.approve_encryption_req, name="appove-encryption-request"),

    path(r'encryption_requests/<int:id>/delete-data-item', views.delete_data_from_encryption_req, name='delete-data-from-request'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
]
