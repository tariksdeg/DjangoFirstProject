from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission,User

# class CustomUser(AbstractUser):
#     ADMIN="ADMIN"
#     BLOGGER="BLOGGER"
#     USER_ROLES=[
#         (ADMIN,"Admin"),
#         (BLOGGER,"Blogger"),
#     ]
#     role = models.CharField(max_length=255,choices=USER_ROLES,default=ADMIN)

#     groups = models.ManyToManyField(Group, related_name='custom_user_groups2')
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions2')
#     # USERNAME_FIELD = 'email'

# class CustomUser(AbstractUser):
    # role = models.CharField(max_length=255,default = "BLOGGER")
    # password = models.CharField(max_length=255)
    # username = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255)    

    # groups = models.ManyToManyField(Group, related_name='blogger_user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='blogger_user_permissions')

# class CustomUser(User):
# class CustomUser(AbstractUser):
#     ADMIN = "ADMIN"
#     BLOGGER = "BLOGGER"
#     USER_ROLES = [
#         (ADMIN, "Admin"),
#         (BLOGGER, "Blogger"),
#     ]
#     role = models.CharField(max_length=255, choices=USER_ROLES, default=ADMIN)

class CustomUser(AbstractUser):
    ADMIN = "ADMIN"
    BLOGGER = "BLOGGER"
    USER_ROLES = [
        (ADMIN, "Admin"),
        (BLOGGER, "Blogger"), 
    ]
    role = models.CharField(max_length=255, choices=USER_ROLES, default=ADMIN)

class Makale(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()