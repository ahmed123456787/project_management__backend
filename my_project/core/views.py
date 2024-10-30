from django.core.mail import BadHeaderError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from django.template.loader import render_to_string
import rest_framework.status as status
from django.utils.html import strip_tags
from .models import Project, Task, ProjectMembership
from accounts.permissions import IsAdminOrOwner, IsDeveloper
import rest_framework.viewsets as viewsets
from .serializers import ProjectSerializer, TaskSerializer



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
    
    
    
class TaskViewSet (viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer    