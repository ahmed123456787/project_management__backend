from django.urls import path , include
from rest_framework.routers import SimpleRouter
from .views import ProjectViewSet, SprintViewSet, TaskView


router = SimpleRouter()
router.register("projects", ProjectViewSet)
router.register(r"projects/(?P<project_id>[^/.]+)/sprints", SprintViewSet, basename="sprint")
# task_list = SprintViewSet.as_view({'get': 'list'})
# task__detail =  SprintViewSet.as_view({'get': 'retreive'})

urlpatterns  = [
    path('',include(router.urls)),
    # path('projects/<int:project_id>/sprints/', task_list, name='project-task-list'), 
    path("projects/<int:project_id>/sprints/<int:sprint_id>/tasks/<int:task_id>",TaskView.as_view(),name="task"),
    path("projects/<int:project_id>/sprints/<int:sprint_id>/tasks/", TaskView.as_view(), name="task-list"),
]  