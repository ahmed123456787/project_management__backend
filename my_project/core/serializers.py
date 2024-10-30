from rest_framework.serializers import ModelSerializer ,SerializerMethodField
from .models import *

class TaskSerializer (ModelSerializer) : 
    model = Task 
    fields = "__all__"

class SprintSerializer(ModelSerializer) :
    
    class Meta : 
        model = Sprint
        fields = "__all__"

class ProjectSerializer(ModelSerializer):
    sprints = SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'sprints']

    def get_sprints(self, obj):
        # Use the related_name to retrieve the related sprints
        sprints = obj.projects.all()  # Here, 'projects' is the related name you've assigned
        return SprintSerializer(sprints, many=True).data  # Serialize the sprints


        
    
        

        
class ProjectMembershipSerializer(ModelSerializer) :
    class Meta : 
        model = ProjectMembership
        fields = "__all__"