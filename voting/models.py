from django.db import models
from django.utils.text import slugify

# Create your models here.

class BaseModel(models.Model):
    """
    BaseModel is an abstract base class for Django models that provides
    created_at and updated_at fields to track the creation and modification
    times of model instances.

    Attributes:
        created_at (DateTimeField): The date and time when the instance was created.
        updated_at (DateTimeField): The date and time when the instance was last updated.

    Meta:
        abstract (bool): Indicates that this is an abstract base class and should not be used to create any database table.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Position(BaseModel):
    """
    A model representing a position in the voting system.

    Attributes:
        name (str): The name of the position.
        slug (str): A unique slug for the position, generated from the name if not provided.
        description (str): A description of the position.

    Methods:
        save(*args, **kwargs): Overrides the save method to automatically generate a unique slug if not provided.
        __str__(): Returns a string representation of the position, which is its name.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
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