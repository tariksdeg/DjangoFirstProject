from rest_framework import serializers
from .models import CustomUser,CustomUser

class UserRegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id","username","email","password","role"]
        extra_kwargs = {"password":{"write_only":True}}

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data.get("role",CustomUser.ADMIN)
        )
        return user    

class BloggerUserRegisterSeriliazers(serializers.Serializer):
    role = serializers.CharField(max_length=255,default="BLOGGER")
    password = serializers.CharField(max_length=255,required=True)
    username = serializers.CharField(max_length=255,required=True)
    email = serializers.EmailField(max_length=255,required=True) 

class BloggerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username","email","password","role"]

class UserSerializers(serializers.Serializer):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('BLOGGER', 'Blogger'),
    )
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=ROLE_CHOICES,default="BLOGGER")
            

class LoginViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField(required=False)

    def validate_email(self, value):
	    return value.lower()
    
class MakaleSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3,max_length=10)
    text = serializers.CharField(min_length=10)
class MakaleUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3,max_length=10)
    text = serializers.CharField(min_length=10)
    id = serializers.IntegerField(min_value = 1)    

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value = 1)    
     