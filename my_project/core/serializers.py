from rest_framework.serializers import ModelSerializer ,SerializerMethodField
from .models import *


class TaskSerializer (ModelSerializer) : 
    class Meta :
        model = Task 
        fields = ["id", "name","due_date","remainder_date","status","created_at", "updated_at","sprint"]

class SprintSerializer(ModelSerializer) :
    tasks = TaskSerializer(many=True,read_only=True)
    class Meta :  
        model = Sprint
        fields = ["id", "name", "project","tasks"]

class ProjectSerializer(ModelSerializer):
    sprints = SprintSerializer(many=True,read_only=True) 
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at',"sprints"]

    
class ProjectMembershipSerializer(ModelSerializer):
    project = ProjectSerializer()  # Include the full project details

    class Meta:
        model = ProjectMembership
        fields = ["id", "project", "role", "user"]
        extra_kwargs = {
            "user": {"write_only": True},  
        }
         
