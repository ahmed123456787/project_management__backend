from django.urls import path , include
from rest_framework.routers import SimpleRouter
from .views import ProjectViewSet, TaskViewSet

pr_router = SimpleRouter()
pr_router.register("projects", ProjectViewSet)

tsk_router = SimpleRouter()
tsk_router.register("tasks",TaskViewSet)

urlpatterns  = [
    path('',include(pr_router.urls)),
    path('',include(tsk_router.urls)),
] 