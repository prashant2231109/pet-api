from django.db import models
from django.contrib.auth.models import User
from .choices import ANIMAL_CHOICES,GENDER_CHOICES
import uuid
from django.utils.text import slugify


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    created_at =models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    
    
    class Meta:
        abstract=True   #treated as class not model if we dont do this then django create a model of this in database


class AnimalBreed(BaseModel):
    breed_name=models.CharField(max_length=100)
    def __str__(self):
        return self.breed_name
    
class AnimalColor(BaseModel):
    animal_color=models.CharField(max_length=100)  
    def __str__(self):
        return self.animal_color
    
class Category(BaseModel):
    category_name=models.CharField(max_length=100)   
    def __str__(self):
        return self.category_name   

class Animal(BaseModel):
    animal_owner =models.ForeignKey(User,on_delete=models.CASCADE,related_name="animals")                         #model cascade ky akrta hai agr parent delte hua to sb uske related delter ho jayega
    animal_category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="animals_category")                                         #related name -for reverse realtionship  
    animal_views =models.IntegerField(default=0)
    animal_likes=models.IntegerField(default=1)
    animal_name=models.CharField(max_length=100)     
    animal_description=models.TextField()
    animal_slug=models.SlugField(max_length=1000,unique=True,blank=True)
    animal_gender=models.CharField(max_length=100,choices=GENDER_CHOICES)
    animal_breed=models.ManyToManyField(AnimalBreed,blank=True)
    animal_color=models.ManyToManyField(AnimalColor,blank=True)
    
    def save(self, *args, **kwargs):
        uid=str(uuid.uuid4()).split('-')
        self.animal_slug=slugify(self.animal_name)+uid[0]
        super(Animal,self).save(*args,**kwargs)
    
    
    def incrementViews(self):
        self.animal_views +=1
        self.save()
    
    def incrementLikes(self):
        self.animal_likes +=1
        self.save()
        
        
    def __str__(self):
        return self.animal_name
    
    
    
    
class AnimalLocation(BaseModel):
    animal=models.ForeignKey("Animal", on_delete=models.CASCADE,related_name="location")
    location=models.CharField(max_length=100)
    
    def __str__(self):
        return self.location
    
    
class AnimalImages(BaseModel):
    animal=models.ForeignKey("Animal", on_delete=models.CASCADE,related_name="images")
    animal_image=models.ImageField(upload_to="animals")   
    
    def __str__(self):
        return f"Image of {self.animal.animal_name}" 
                            
    
