from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Projects, Contributors


class ProjectPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class ContributorPermissions(BasePermission):

    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs['project_pk'])
        if request.method == 'POST':
            return project.author_user == request.user
        return True

    def has_object_permission(self, request, view, obj):
        project = Projects.objects.get(id=view.kwargs['project_pk'])
        if request.method in SAFE_METHODS:
            return True
        return project.author_user == request.user


class IssuePermissions(BasePermission):

    def has_permission(self, request, view):
        contributors = []
        for contributor in Contributors.objects.filter(project=view.kwargs['project_pk']):
            contributors.append(contributor.user)
        return request.user in contributors

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user


class CommentPermissions(BasePermission):

    def has_permission(self, request, view):
        contributors = []
        for contributor in Contributors.objects.filter(project=view.kwargs['project_pk']):
            contributors.append(contributor.user)
        return request.user in contributors

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user == request.user
