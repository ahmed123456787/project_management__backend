from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.template.loader import render_to_string
import rest_framework.status as status
from django.utils.html import strip_tags
from .models import Project, Sprint, ProjectMembership, Task
from accounts.permissions import IsAdminOrOwner, IsDeveloper
import rest_framework.viewsets as viewsets
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer, ProjectMembershipSerializer
from rest_framework.viewsets import generics
from accounts.permissions import IsAdminOrOwner, IsDeveloper
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound


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
    queryset = ProjectMembership.objects.all()
    serializer_class = ProjectMembershipSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def _pop_user_field(self, projects_membership):
        """Remove the user from project membership"""
        for project in projects_membership:
            project.pop("user", None)  # Use `None` to avoid KeyError if user is missing
        return projects_membership

    def get_serializer_class(self):
        if self.action in ["create","update","partial_update"]:
            return ProjectSerializer
        else:
            return self.serializer_class
      
    def get_permissions(self):
        
        if self.action in ['update',"partial_update"]:
            permission_classes = [IsAuthenticated,IsAdminOrOwner]
        else:
            permission_classes = [IsAuthenticated]    
        return [permission() for permission in permission_classes]    
        
    def list(self, request, *args, **kwargs):
        """List all project memberships for the authenticated user"""
        project_members = ProjectMembership.objects.filter(user=self.request.user) 
        serializer = ProjectMembershipSerializer(project_members, many=True)
        
        # Remove the user field from each project membership
        data = serializer.data
        # data = self._pop_user_field(data)
    
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single project by ID."""
        project_id = kwargs.get("pk")  # Get the project ID from the URL
        try:
            # Filter ProjectMembership by user and project ID
            membership = ProjectMembership.objects.get(
                project_id=project_id,
                user=request.user
            )
            # Serialize and return the project data
            serializer = ProjectSerializer(membership.project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProjectMembership.DoesNotExist:
            return Response(
                {"message": "You are not a member of this project."},
                status=status.HTTP_404_NOT_FOUND
            )


    def create(self, request, *args, **kwargs):
        """Create a new project and automatically assign the user as an admin"""
        # Step 1: Validate and save the project data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        project = serializer.save(user=self.request.user)

        # Step 3: Create a ProjectMembership entry for the user who created the project
        ProjectMembership.objects.create(
            project=project,
            user=request.user,  # Assuming the user is the one making the request
            role='admin'  # Assign the 'admin' role to the user
        )

        # Step 4: Return the response with the serialized data and status code
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Return projects where the user is either the creator or a member.
        """
        user = self.request.user

        # Projects created by the user
        owned_projects = Project.objects.filter(user=user)

        # Projects where the user is a member
        member_projects = Project.objects.filter(memberships__user=user)

        # Combine and remove duplicates
        return owned_projects

    def get_object(self):
            """
            Retrieve a specific project by ID, ensuring the user has access.
            """
            project_id = self.kwargs.get("pk")  # Get the 'id' from the URL route
            user = self.request.user

            try:
                # Filter the project by ID and ensure the user is either the creator or a member
                project = Project.objects.filter(
                    id=project_id, 
                    user=self.request.user
                ).distinct().get()
            except Project.DoesNotExist:
                raise NotFound({"detail": "Project not found or you don't have access."})

            return project
    
    def update(self, request, *args, **kwargs):
        """Update a project."""
        print(self.action)
        partial = kwargs.pop('partial', False)  # Support both PUT and PATCH
        instance = self.get_object()  # Fetch the specific project
        print(self.get_serializer_class())
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


    
class SprintViewSet(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        # Ensure this filters by the user properly
        return Sprint.objects.filter(project__user=self.request.user)
        
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