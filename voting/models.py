from django.db import models

# Create your models here.


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    image = models.ImageField(upload_to='candidates')
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.vote}"
    

class Voter(models.Model):
    matric_number = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.matric_number}"