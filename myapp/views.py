from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CanAddBloggerUser, JustBlogger
from .serializers import IdSerializer, LoginViewSerializer, MakaleSerializer, MakaleUpdateSerializer, UserSerializers, UserRegisterSerializers,BloggerUserRegisterSeriliazers,BloggerUserSerializer
from .models import CustomUser, Makale
from .methods import getBloggerMakale, newBloggerUser
from django.contrib.auth import authenticate,get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.contrib.auth.hashers import make_password

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        print("serializer",serializer)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            password = make_password(serializer.validated_data["password"])  # Şifreyi güvenli bir şekilde şifrele
            role = serializer.validated_data["role"]

            try:
                CustomUser.objects.create(
                username=username,
                email=email,
                password=password,
                role=role
            )
                return Response({
                "isSuccess": True,
                "message": "CustomUser created successfully",
                "data": serializer.data
            }, status=200)
            except Exception as e:
                Response({
            "isSuccess": False,
            "message": e
        }, status=500)

            

            
        return Response({
            "isSuccess": False,
            "message": serializer.errors
        }, status=400)

# class UserLoginView(APIView):
#     permission_classes = [AllowAny,]

#     def post(self, request):
#         serializer = LoginViewSerializer(data = request.data)
#         if not serializer.is_valid():
#             return Response({
#                 'success' : False,
#                 'message' : 'Something went wrong',
#                 'data' : serializer.errors,
#             },status=400)
#         user = authenticate(email = serializer.data['email'], password = serializer.data['password'])
#         print("user",user)
#         if user is None:
#             return Response({
# 					'success' : False,
# 					'message' : 'Invalid credentials',
# 					'data' : {}
# 				}, status= 401)
        
#         response_data = {}
#         refresh = RefreshToken.for_user(user)
#         response_data = {
# 					'refresh' : str(refresh),
# 					'access' : str(refresh.access_token)
# 				}
#         return Response({
# 				'success' : True,
# 				'role' : user.role,
# 				'data' : response_data
# 			})
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginViewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Something went wrong',
                'data': serializer.errors,
            }, status=400)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        # user = CustomUser.objects.filter(email=email).first()
        print("user",user)
        if user is None:
            return Response({
                'success': False,
                'message': 'Invalid credentials',
                'data': {}
            }, status=401)

        try:
            print("usertry",user)
            refresh = RefreshToken.for_user(user)
            response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
            return Response({
            'success': True,
            'role': user.role,
            'data': response_data
        })
        except Exception as e:
            return Response({
				'success' : False,
				'message' : f"Something went wrong {e}",
			}, status= 500)

        

        

        
    
class BloggerUserRegisterView(APIView):
    permission_classes = [IsAuthenticated,CanAddBloggerUser]
    authentication_classes = (JWTAuthentication,)

    def post(self,request):
        serializer = BloggerUserRegisterSeriliazers(data=request.data)
        if serializer.is_valid():
            print("serializer",serializer.data)
            # serializer.save()
            response,status = newBloggerUser(serializer.data,request.data)
            return Response(response,status=status)
        return Response({
            "isSuccess":False,
            "message":serializer.errors,

        },status=400)
    
    def get(self, request):
        id_params = request.query_params.get("id")
        if id_params:
            try:
                user = CustomUser.objects.get(id=id_params)
                serializer = BloggerUserSerializer(user)
                data = serializer.data
                return Response({
                    "isSuccess": True,
                    "data": data,
                }, status=200)
            except CustomUser.DoesNotExist:
                return Response({
                    "isSuccess": False,
                    "message": "CustomUser not found with the given id",
                }, status=404)
        else:
            users = CustomUser.objects.all()
            serializer = BloggerUserSerializer(users, many=True)
            data = serializer.data
            return Response({
                "isSuccess": True,
                "data": data,
            }, status=200)
    
    def delete(self, request):
        id_param = request.query_params.get("id")
        if id_param:
            try:
                user = CustomUser.objects.get(id=id_param)
                user.delete()
                return Response({"isSuccess": True, "message": "Kullanıcı başarıyla silindi."}, status=200)
            except CustomUser.DoesNotExist:
                return Response({"isSuccess": False, "message": "Belirtilen ID'ye sahip kullanıcı bulunamadı."}, status=404)
        else:
            return Response({"isSuccess": False, "message": "ID parametresi belirtilmedi."}, status=400)
    
    def put(self,request):
        id_params = request.data["id"]
        if id_params:
            try:
                user = CustomUser.objects.get(id=id_params)
                serializer = BloggerUserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"isSuccess": True, "message": "Kullanıcı bilgileri başarıyla güncellendi.","data":serializer.data}, status=200)
                return Response(serializer.errors, status=400)
            except CustomUser.DoesNotExist:
                return Response({"isSuccess": False, "message": "Belirtilen ID'ye sahip kullanıcı bulunamadı."}, status=404)
        else:
            return Response({"isSuccess": False, "message": "ID parametresi belirtilmedi."}, status=400)


        
class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("email", email)
        print("settings.AUTH_USER_MODEL", settings.AUTH_USER_MODEL)
        # try:
        user = CustomUser.objects.filter(email=email).first()
        print("userbackend",user)
        if not user:
            return None
        else:
            print("girdi")
            if user.check_password(password):
                print("girdi2")
                return user
            return None
        # except CustomUser.DoesNotExist:
        # else:
        #     if user.check_password(password):
        #         return user
        # return None
        
# class EmailBackend(ModelBackend):
# 	def authenticate(self, request, email=None, password=None, **kwargs):
# 		UserModel = get_user_model()
# 		try:
# 			user = UserModel.objects.get(email=email)
# 		except UserModel.DoesNotExist:
# 			return None
# 		else:
# 			if user.check_password(password):
# 				return user
# 		return None        
        
class MakeleView(APIView):
    permission_classes = [IsAuthenticated, JustBlogger]
    authentication_classes = (JWTAuthentication,)

    def get(self,request):
        query_params=request.query_params
        if query_params:
            serializer = IdSerializer(data=query_params)
            if not serializer.is_valid():
                return Response({
				    'success' : False,
				    'message' : 'Something went wrong',
				    'data' : serializer.errors,
			    }, status= 400)
            
            user_obj = CustomUser.objects.filter(id=serializer.data["id"]).first()
            if not user_obj:
                return Response({
                    "success":False,
                    "message":"Customer account not found",
                    "data":{"user_id": serializer.data["id"]}
                },status=400)

            response,status = getBloggerMakale(user_obj,request.user,False)
            return Response(response,status)
        response,status = getBloggerMakale(None,request.user,True)
        return Response(response,status)

    def post(self, request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Makale.objects.create(
                    user=request.user,
                    title=serializer.data["title"],
                    text=serializer.data["text"]
                )
                return Response({
                    "isSuccess": True,
                    "data": serializer.data,
                }, status=200)
            
            except Exception as e:
                return Response({
                    "isSuccess": False,
                    "data": str(e),  
                }, status=500)
            
        return Response({
            "isSuccess": False,
            "data": serializer.errors,
        }, status=400)
    
    def delete(self,request):
        query_params=request.query_params
        serializer = IdSerializer(data=query_params)
        if not serializer.is_valid():
            return Response({
				    'success' : False,
				    'message' : 'Something went wrong',
				    'data' : serializer.errors,
			    }, status= 400)
        makale = Makale.objects.filter(id=serializer.data["id"]).first()
        if not makale:
            return Response({
				    'success' : False,
				    'message' : 'Makale not found',
			    }, status= 400)
        if makale.user == request.user:
            makale.delete()
            return Response({
				    'success' : True,
                    "message":"Makale deleted"
			    }, status= 200)
        return Response({
			    'success' : False,
                "message":"You don't have permission"
		    }, status= 403)

    def put(self,request):
        serializer = MakaleUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
				    'success' : False,
				    'message' : 'Something went wrong',
				    'data' : serializer.errors,
			    }, status= 400)
        makale = Makale.objects.filter(id=serializer.data["id"]).first()
        if makale.user == request.user:
            makale.text=serializer.data["text"]
            makale.title=serializer.data["title"]
            makale.save()
            return Response({
	    	    'success' : True,
	    	    'message' : 'Updated succesfully',
	    	    'data' : {
                    "text":makale.text,
                    "title":makale.title,
                },
	    	}, status= 400)
        return Response({
	        'success' : False,
	        'message' : "You don't have permission",
	    }, status= 403)