from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.template.loader import render_to_string
import rest_framework.status as status
from django.utils.html import strip_tags
from .models import Project, Sprint, ProjectMembership, Task
from accounts.permissions import IsAdminOrOwner, IsDeveloper
import rest_framework.viewsets as viewsets
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import mixins
from rest_framework.viewsets import generics

class SendInvitationEmail(APIView):
    def post(self, request):
        recipient_email = request.data.get("email", "ahmed.zater@univ-constantine2.dz")
        
        html_content = render_to_string(
            "email.html",
        )
        plain_message = strip_tags(html_content)
        
        msg = EmailMultiAlternatives(
            body=plain_message,
            subject="You have been invited to the project board",
            from_email="zaterahmed62@gmail.com",  # Sender's email address
            to=[recipient_email],  # Recipient email(s)
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        print(msg.send())
        return Response({"message": "Invitation email sent!"}, status=status.HTTP_200_OK)

        
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
 
    def retrieve(self, request, *args, **kwargs):
        # Check if the project exists
        instance = self.get_object()
        if not instance:
            return Response(
                {"message": "No projects found with the given ID"},
                status=status.HTTP_404_NOT) 
        serializer = ProjectSerializer(instance)    
        return Response(serializer.data,status=status.HTTP_200_OK)  
    def create(self, request, *args, **kwargs):
        # Step 1: Get the data from the request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        project = serializer.save()
        
        # Step 3: Create a ProjectMembership entry for the user who created the project
        ProjectMembership.objects.create(
            project=project,
            user=request.user,  # Assuming the user is the one making the request
            role='admin'  # Assign the role as per your requirement
        )

        # Step 4: Return the response with the serialized data and status code
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    
   
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
        
    
class SprintsProjectView(generics.ListAPIView,
                         generics.RetrieveAPIView):
    """Viewset for sprints for a specific project and for specific sprints"""
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    
    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        sprint_id = self.kwargs.get("sprint_id")

        queryset = Sprint.objects.filter(project_id=project_id)
        if sprint_id:
            queryset = queryset.filter(id=sprint_id)
        return queryset
        
        
class TasksProjectSprintView(generics.ListAPIView):
    """View to get a list of tasks depending on project and sprints"""
    
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        sprint_id = self.kwargs.get("sprint_id")
        task_id = self.kwargs.get("task_id")

        # Filter tasks by sprint and project
        queryset = Task.objects.filter(sprint__project_id=project_id, sprint_id=sprint_id)

        # Further filter by task ID if provided
        if task_id:
            queryset = queryset.filter(id=task_id)
        
        return queryset

        
        