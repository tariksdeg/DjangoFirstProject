from rest_framework.permissions import BasePermission

class CanAddBloggerUser(BasePermission):
    def has_permission(self, request, view):
        print("req",request)
        return request.user.role == 'ADMIN'
    pass
class JustBlogger(BasePermission):
    def has_permission(self, request, view):
        print("req",request)
        return request.user.role == 'BLOGGER'
    pass
