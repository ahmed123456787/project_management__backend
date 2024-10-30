import rest_framework.permissions  as permissions
from core.models import ProjectMembership 
 
# class Admin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name="admin").exists():
#             return True    


# class Developer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name="developper").exists():
#             return True 
        
        
# class Viewer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.groups.filter(name="viewer").exists():
#             return True                 
        
        
        


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is an admin or owner of the project.
    """

       
    def has_object_permission(self, request, view, obj):
        # Allow the owner to access the project as well as admins
        print(request)
        if request.user == obj.owner:
            return True
        
        # Check if the user is an admin
        membership = ProjectMembership.objects.filter(project=obj, user=request.user).first()
        if membership and membership.role == 'admin':
            return True

        return False

class IsDeveloper(permissions.BasePermission):
    """
    Custom permission to allow developers and admins to modify a project.
    """

    def has_object_permission(self, request, view, obj):
        membership = ProjectMembership.objects.filter(project=obj, user=request.user).first()
        if membership and membership.role in ['developer']:
            return True
        return False