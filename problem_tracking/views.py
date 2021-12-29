from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as Auth_user
from rest_framework.response import Response

from .serializers import ProjectSerializer, RegisterSerializer, ContributorSerializer, IssueSerializer
from .models import Projects, Contributors, Issues
from .permissions import ProjectPermissions, ContributorPermissions, IssuePermissions


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = Auth_user.objects.all()
        return queryset


class ProjectsViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ProjectPermissions]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.filter(contributor_project__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid()
        project = serializer.save(author_user=request.user)
        Contributors.objects.create(user=request.user, project=project, role='AUTHOR')
        return Response(serializer.data)


class ContributorsViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ContributorPermissions]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):

        serializer = ContributorSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(project=Projects.objects.get(pk=self.kwargs['project_pk']))
        return Response(serializer.data)


class IssuesViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IssuePermissions]
    serializer_class = IssueSerializer

    def get_renderers(self):
        return Issues.objects.filter(project=self.kwargs['project_pk'])

