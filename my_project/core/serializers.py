from rest_framework.serializers import ModelSerializer ,PrimaryKeyRelatedField
from .models import *

class TaskSerializer(ModelSerializer) :
    class Meta : 
        model = Task
        fields = "__all__"

class ProjectSerializer(ModelSerializer) :
    task = PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta :  
        model = Project
        fields = "__all__"
        
    
        

        
class ProjectMembershipSerializer(ModelSerializer) :
    class Meta : 
        model = ProjectMembership
        fields = "__all__"