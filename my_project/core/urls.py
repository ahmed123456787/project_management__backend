from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, SprintViewSet, TaskViewSet, SprintsProjectView, TasksProjectSprintView


router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("sprints",SprintViewSet)
router.register("tasks",TaskViewSet)

urlpatterns  = [
    path('',include(router.urls)),
    path("projects/<int:project_id>/sprints/",
         SprintsProjectView.as_view(),
         name="project-sprints",
    ),
        path(
        "projects/<int:project_id>/sprints/<int:sprint_id>/",
        SprintsProjectView.as_view(),
        name="project-sprint-detail",
    ),
    path(
        "projects/<int:project_id>/sprints/<int:sprint_id>/tasks/",
        TasksProjectSprintView.as_view(),
        name="project-sprint-detail",
    ),
    path(
        "projects/<int:project_id>/sprints/<int:sprint_id>/tasks/<int:task_id>/",
        TasksProjectSprintView.as_view(),
        name="project-sprint-detail",
    ),
]   