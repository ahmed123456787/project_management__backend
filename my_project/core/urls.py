from django.urls import path , include
from rest_framework.routers import SimpleRouter
from .views import ProjectViewSet, SprintViewSet

pr_router = SimpleRouter()
pr_router.register("projects", ProjectViewSet)

task_list = SprintViewSet.as_view({'get': 'list'})


urlpatterns  = [
    path('',include(pr_router.urls)),
    path('projects/<int:project_id>/sprints/', task_list, name='project-task-list'), 
] 