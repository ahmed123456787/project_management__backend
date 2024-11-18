from django.db import models
from accounts.models import User
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'user')
    
    def __str__(self):
        return self.name
  
    
class Sprint(models.Model):
    name = models.CharField(max_length=200,unique=True)
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='sprints',  # Updated related_name
    )
    
    def __str__(self):
        return self.name 
    
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ("in progress", "In Progress"),
        ("done", "Done"),   
    ]
    
    name = models.CharField(max_length=100,unique=True)
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="tasks")
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    remainder_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to do")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Comment(models.Model):
    comment = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class CheckTask(models.Model):
    name = models.CharField(max_length=200)
    tasks = models.ForeignKey(Task, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_checked = models.BooleanField()
     
class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),  
        ('developer', 'Developer'),  
        ('viewer', 'Viewer'),  
    ]
     
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships", null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", null=True, blank=True, default=None)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        unique_together = ('project', 'user')
    
    def __str__(self):
        return f"{self.user.name} as {self.role} in {self.project.name}"
