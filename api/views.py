
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from rest_framework import viewsets
from .serializers import TaskSerializer
# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)