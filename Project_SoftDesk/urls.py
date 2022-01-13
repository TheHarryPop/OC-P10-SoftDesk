from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from problem_tracking.views import ProjectsViewSet, RegisterView, ContributorsViewSet, IssuesViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register('projects', ProjectsViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('users', ContributorsViewSet, basename='users')
projects_router.register('issues', IssuesViewSet, basename='issues')

issues_router = routers.NestedSimpleRouter(projects_router, 'issues', lookup='issue')
issues_router.register('comments', CommentsViewSet, basename='comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/-auth', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', RegisterView.as_view(), name='auth_signup'),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(issues_router.urls))
]
