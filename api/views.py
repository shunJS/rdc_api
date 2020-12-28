from django_cognito_jwt import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from rest_framework import viewsets
from .serializers import TaskSerializer
# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)