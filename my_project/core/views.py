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
from rest_framework.generics import RetrieveUpdateDestroyAPIView


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
        # except BadHeaderError:
        #     return Response({"error": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # def get_permissions(self):
        
    #      """
    #      Assign custom permissions based on the action being performed.
    #      """
    #      if self.action in ['create','update', 'partial_update','destroy']:
    #         permission_classes = [IsAdminOrOwner]
             
    #      else:  # Default to read-only access for retrieve and list actions
    #         permission_classes = [IsAdminOrOwner | IsDeveloper]
    #      return [permission() for permission in permission_classes]     
            
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No projects found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  
          
    def create(self, request, *args, **kwargs):
        # Step 1: Get the data from the request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Step 2: Save the new project instance
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
    serializer_class = SprintSerializer

    def get_queryset(self):
        
        project_id = self.kwargs.get('project_id')
        if project_id:
            # Filter sprints based on the project ID
            return Sprint.objects.filter(project_id=project_id)
        # Default to all sprints if no project_id is specified
        return Sprint.objects.all()

    def retrieve(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        sprint_id = self.kwargs.get('pk')  # This is usually passed as 'pk' for retrieve actions
        
        # Try to fetch the sprint with the specific project and sprint ID
        try:
            sprint = Sprint.objects.get(id=sprint_id, project_id=project_id)
            serializer = self.get_serializer(sprint)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sprint.DoesNotExist:
            return Response({"error": "Sprint not found"}, status=status.HTTP_404_NOT_FOUND)

class TaskView(APIView):
 
    def get(self, request, project_id, sprint_id, task_id=None):
        
        try:
            # Get the sprint, ensuring it belongs to the specified project
            sprint = Sprint.objects.get(id=sprint_id, project_id=project_id)
            
            # Filter tasks within the sprint
            if task_id:
                task = Task.objects.get(id=task_id, sprint=sprint)
                serializer = TaskSerializer(task)
                # serializer.is_valid()
                # print(serializer.errors)
            else:
                tasks = Task.objects.filter(sprint=sprint)
                
                serializer = TaskSerializer(tasks, many=True)
             
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (Sprint.DoesNotExist, Task.DoesNotExist):
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)