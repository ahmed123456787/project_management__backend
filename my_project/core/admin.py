from django.contrib import admin
from .models import Project, ProjectMembership, Task, Comment, Sprint, CheckTask

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(ProjectMembership)
admin.site.register(Sprint)
admin.site.register(Comment)
admin.site.register(CheckTask)

 