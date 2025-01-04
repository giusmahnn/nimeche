from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Position(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)


class Candidate(BaseModel):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.vote}"
    

class Voter(BaseModel):
    matric_number = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.matric_number}"