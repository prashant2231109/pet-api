from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




    
    
    
    
class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalBreed
        fields="__all__"
        


class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalColor
        fields=['animal_color']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['category_name',]  #jo field rakhna uska name rakho bahe serilaize hoga bake hide ho jeyga

class AnimalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalImages
        fields="__all__"
        
class AnimalSerializer(serializers.ModelSerializer):
    # animal_category =CategorySerializer()  #one method but agr agr jisme jab dikhaega categogry har chiz but sirf hame name dikahna hai to second method
    animal_category=serializers.SerializerMethodField() #second method
    animal_color=AnimalColorSerializer( many=True ) #this is a way to serilaize many serilaizer
    animal_breed=AnimalBreedSerializer(many=True)
    
    
    # images=AnimalImagesSerializer(many=True)  why hide because abhe ke liye image filed ko nhe behjna hai backend me temperory for tresting
    def get_animal_category(self,obj):   #ye jo def ake age get underscore likhna jaruri hai second method hai
        return obj.animal_category.category_name  
    
    def create(self, data):
        print(data)
        animal_breed=data.pop('animal_breed')
        animal_color=data.pop('animal_color')
        animal=Animal.objects.create(**data,animal_category=Category.objects.get(category_name="Dog"))
        
        for ab in animal_breed:
            animal_breed_obj=AnimalBreed.objects.get(breed_name=ab['breed_name'])
            animal.animal_breed.add(animal_breed_obj)
        
    
        for ac in animal_color:
            animal_color_obj=AnimalColor.objects.get(animal_color=ac['animal_color'])
            animal.animal_color.add(animal_color_obj)
            
            
        return animal
    
    def update(self,instance,data):
        if 'animal_breed' in data:
            animal_breed=data.pop('animal_breed')
            instance.animal_breed().clear()
            for ab in animal_breed:
                animal_breed_obj=AnimalBreed.objects.get(breed_name=ab['breed_name'])
                instance.animal_breed.add(animal_breed_obj)
    
        if 'animal_color' in data:
            animal_color=data.pop('animal_color')
            
        instance.animal_name=data.get('animal_name',instance.animal_name)
        instance.animal_description=data.get('animal_description',instance.animal_description)
        instance.animal_gender=data.get('animal_gender',instance.animal_gender) 
        
        instance.save()
        return instance    
        
        
    class Meta:
        model=Animal
        exclude =['updated_at']


class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnimalLocation
        fields="__all__"
        
        
        
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()  
    
    def validate(self,data):
        
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            
            if user.exists():
                raise serializers.ValidationError('username is alrealy taken')
            
            
            
        if 'email' in data:
            user=User.objects.filter(email=data['email'])
            
            if user.exists():
                raise serializers.ValidationError('email is alrealy taken')
            
            
            
            
            
            
        return data    
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,data):
        
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            
            if not user.exists():
                raise serializers.ValidationError('username does not exists')
          
          
        return data




