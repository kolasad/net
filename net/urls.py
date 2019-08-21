from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from files import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/create/', views.FileHolderCreateView.as_view(), name='files-create'),
    path('files/<slug:slug>/', views.FileHolderDetailView.as_view(), name='files-detail'),
    path('urls/create/', views.UrlHolderCreateView.as_view(), name='urls-create'),
    path('urls/<slug:slug>/', views.UrlHolderDetailView.as_view(), name='urls-detail'),
]

# API urls
router = DefaultRouter()
router.register(r'files', views.FileViewSet)
router.register(r'urls', views.UrlViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/<int:pk>/download/', views.FileViewSet.as_view({"get": "download"}))
]
