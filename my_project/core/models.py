from django.db import models
from accounts.models import CustomUser 


class Task(models.Model):
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ("in progress", "In Progress"),
        ("done", "Done"),   
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()  # Using TextField for longer descriptions
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to do")
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when task is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when task is updated

    def __str__(self):
        return f"{self.name} "


class Project(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name="task",default=None)
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),  
        ('developer', 'Developer'),  
        ('viewer', 'Viewer'),  
    ]
     
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        unique_together = ('project', 'user')  # Ensures unique role per user per project
    
    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.project.name}"

   