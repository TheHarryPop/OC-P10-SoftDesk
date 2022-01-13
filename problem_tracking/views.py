from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User as Auth_user
from rest_framework.response import Response

from .serializers import ProjectListSerializer, ProjectDetailSerializer, RegisterSerializer, \
    ContributorListSerializer, ContributorDetailSerializer, IssueListSerializer, IssueDetailSerializer, \
    CommentListSerializer, CommentDetailSerializer
from .models import Projects, Contributors, Issues, Comments
from .permissions import ProjectPermissions, ContributorPermissions, IssueCommentPermissions


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = Auth_user.objects.all()
        return queryset


class ProjectsViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ProjectPermissions]
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Projects.objects.filter(contributor_project__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ProjectDetailSerializer(data=request.data)
        serializer.is_valid()
        project = serializer.save(author_user=request.user)
        Contributors.objects.create(user=request.user, project=project, role='AUTHOR')
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorsViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, ContributorPermissions]
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        serializer = ContributorDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(project=Projects.objects.get(pk=self.kwargs['project_pk']), id=request.data['user'])
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class IssuesViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        serializer = IssueDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(project=Projects.objects.get(pk=self.kwargs['project_pk']), author_user=request.user,
                        assignee_user=request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentsViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IssueCommentPermissions]
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comments.objects.filter(issue=self.kwargs['issue_pk'])

    def create(self, request, *args, **kwargs):
        serializer = CommentDetailSerializer(data=request.data)
        serializer.is_valid()
        serializer.save(author_user=request.user, issue=Issues.objects.get(pk=self.kwargs['issue_pk']))
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
