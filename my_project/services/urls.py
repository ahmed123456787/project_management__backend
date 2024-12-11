from django.urls import path
from .views import *

urlpatterns = [
    path("issue",view=create_issue_view,name="issue")
]
