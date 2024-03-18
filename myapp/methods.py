from django.contrib.auth.hashers import make_password
from .models import CustomUser,Makale
from .serializers import MakaleSerializer
def newBloggerUser(data, owner):
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if CustomUser.objects.filter(email=email).exists():
        return {
            'success': False,
            'message': 'Bad Request',
            'data': {'email': ["Email is already in use."]}
        }, 400

    CustomUser.objects.create(
        username=username,
        email=email,
        password=password,  
        role=role  
    )
    return {
        'success': True,
        'message': 'CustomUser created successfully',
        'data': {
        "username":username,
        "email":email,
        }
    }, 200

def getBloggerMakale(user_obj,owner,all):
    if not all:
        user_makale = Makale.objects.filter(user=user_obj).values("title","text","id")
        user_makale = list(user_makale)
        makales = []
        for makale in user_makale:
            serializer = MakaleSerializer(data={'title': makale["title"], 'text': makale["text"]})
            if not serializer.is_valid():
                return {
                    "success":False,
                    "message":"Makale not found",
                },400
            makales.append(
                {
                    "makale_id":makale["id"],
                    "title":makale["title"],
                    "text":makale["text"],
                    "user":{
                        "email":user_obj.email,
                        "username":user_obj.username,
                    }
                }
            )
        return {
                    "success":True,
                    "data":makales,
            },200
    user_makale = Makale.objects.all()
    makales = []
    for makale in user_makale:
         serializer = MakaleSerializer(data={'title': makale.title, 'text': makale.text})
         if not serializer.is_valid():
            return {
                "success":False,
                "message":"Makale not found",
                "data":serializer.errors,
            },400
         makales.append(
            {
                "makale_id":makale.id,
                "title":makale.title,
                "text":makale.text,
                "user":{
                    "email":makale.user.email,
                    "username":makale.user.username
                }
            }
        )
    return {
                "success":True,
                "data":makales,
        },200