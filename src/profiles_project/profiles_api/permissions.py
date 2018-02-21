from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit thier own profile"""
    def has_object_permission(self,request,view,obj):
        """Check user is trying to edit thier own profile"""
        #Here we use the safe method list as specified by the 
        #rest framework
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
class PostOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""
    def has_object_permission(self,request,view,obj):
        """Check if the user is trying to update thier own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id
