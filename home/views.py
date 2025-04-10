from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Animal)
from .serializers import (AnimalSerializer,RegisterSerializer,LoginSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status





class AnimalDetailView(APIView):
    def get(self,request,pk):
        try:
            queryset=Animal.objects.get(pk=pk)
            queryset.incrementViews()
            # queryset.incrementLikes()  #ek animal ka to ek he like de paaoge na logicaly socho to
            serializer=AnimalSerializer(queryset)
            return Response({
            'status':True,
            'message':'animal fetched with Get',
            'data:':serializer.data
        })
        except Exception as e:
            print(e)    
            
            return Response({
            'status':False,
            'message':'somethind went wron',
            'data:':{}
        })
            


class AnimalView(APIView):
    
    def get(self,request):
        queryset=Animal.objects.all()
        
        if request.GET.get('search'):
            search=request.GET.get('search')
            queryset=queryset.filter(
                Q(animal_name__icontains=search)|
                Q(animal_category__category_name__icontains=search)|
                Q(animal_description__icontains=search)|
                Q(animal_gender__iexact=search)|           #iexact is used for case sensitive search or particular search like male or female            
                Q(animal_breed__breed_name__icontains=search)|
                Q(animal_color__animal_color__icontains=search)
            )
        serializer=AnimalSerializer(queryset, many=True)
        
        return Response({
            'status':True,
            'message':'animal fetched with Get',
            'data:':serializer.data
        })
        
        
        
    def post(self,request):
        return Response({
            'status':True,
            'message':'animal fetched with Post',
        })
        
        
        
    def put(self,request):
        return Response({
            'status':True,
            'message':'animal fetched with PUT',
        })
    
    def Patch(self,request):
        return Response({
            'status':True,
            'message':'animal fetched with Patch',
        })  
        
        
class RegisterAPI(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)
            if serializer.is_valid():
                
                user =User.objects.create(
                    username=serializer.data['username'],
                    email=serializer.data['email']
                )
                user.set_password(serializer.data['password'])
                user.save()
                return Response({
                    'status':True,
                    'message':'user created',
                    'data':{}
                })
                
                
            return Response({
                    'status':False,
                    'message':'key error',
                    'data':serializer.errors
                })
                
        except Exception as e:
            print(e)        
        
class LoginAPI(APIView):
    def  post(self, request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if serializer.is_valid():
                user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
                if user:
                    token = Token.objects.get_or_create(user=user)

                    return Response({
                        'message':'login successfully',
                        'status':'True',
                        'data':{
                            'token':str(token)
                        }
                    })
                
                
                
            return Response({
                    'status':False,
                    'message':'invalid password',
                    'data':serializer.errors
                })
                
        except Exception as e:
            print(e) 
            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                }) 
            
            
            
class AnimalCreateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            request.data['animal_owner']=request.user.id
            
            serializer=AnimalSerializer(data=request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'message':'animal created',
                    'data':serializer.data
                })                 
            return Response({
                    'status':False,
                    'message':'invalid data',
                    'data':serializer.errors
            })
            
        except Exception as e:
            print(e) 
            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                })  
    def patch(self,request):
        try:
            if request.data.get('id') is None:
                return Response({
                    'status':False,
                    'message':'animal id is required',
                    'data':{}
                    
                })
                
            animal_obj =Animal.objects.filter(id=request.data.get('id'))
            
            if not animal_obj.exists():
                return Response({
                    'status':False,
                    'message':'inavlid animal id'
                })
            animal_obj=animal_obj[0]
            serializer=AnimalSerializer(data=request.data)  
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'message':'animal updated',
                    'data':serializer.data
                })                 
            return Response({
                    'status':False,
                    'message':'invalid data',
                    'data':serializer.errors
            })
            
        except Exception as e:
            print(e) 
            return Response({
                    'status':False,
                    'message':'something went wrong',
                    'data':{}
                })            
            
