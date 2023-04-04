from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    symptoms = models.ManyToManyField(Symptom, blank=True)
    disease = models.OneToOneField(Disease, on_delete=models.SET_NULL, null=True, blank=True)
  
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def symptom_exists(self, symptom):
        symptom = symptom.lower()
        return any(symptom == s.name.lower() for s in self.symptoms.all())
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_user_message = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

