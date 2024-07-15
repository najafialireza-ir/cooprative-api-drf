from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == '2'
    
    def has_object_permission(self, request, view, obj):
        return obj.driver.user == request.user
        
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated  
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsDriverCar(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == '2'
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerTransection(BasePermission):
    message = 'permission denied, you not owner'
    
    def has_permission(self, request, view):
        return request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        return obj.wallet.user == request.user


class IsAdminOrIsDriverWriteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated and (request.user.is_superuser or request.user.is_driver)
        return request.user

    def has_object_permission(self, request, view, obj):
        return request.user.is_supersuser or request.user.is_driver
    