from django.urls import path
from . import views


urlpatterns = [
    path('',
         views.DeviceListView.as_view(), name='devices-list'),
    path('<int:pk>/',
         views.DeviceDetailView.as_view(), name='devices-item'),
    path('new/',
         views.DeviceCreateView.as_view(), name='devices-new'),
    path('<int:pk>/edit/',
         views.DeviceUpdateView.as_view(), name='devices-edit'),
    path('<int:pk>/del/',
         views.DeviceDeleteView.as_view(), name='devices-del'),
]
