from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from api.views import TaskViewSet
from . import views

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('', include(router.urls))
]