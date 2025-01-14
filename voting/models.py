from django.db import models
from django.utils.text import slugify

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Position(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Position.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Candidate(BaseModel):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"
    

class Voter(BaseModel):
    matric_number = models.CharField(max_length=50, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    voted_position = models.ManyToManyField(Position, blank=True)

    def __str__(self):
        return f"{self.matric_number}"