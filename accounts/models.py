from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
gender = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]

class User(AbstractUser):
	name = models.CharField(max_length=160, null=True, blank=True)
	email = models.EmailField(blank=False, unique=True)
	mobile = models.CharField(max_length=15, null=True, blank=True)
	gender = models.CharField(max_length=10, choices=gender, default='Male')
	dob = models.DateField(null=True, blank=True)
	created_time = models.DateTimeField(auto_now_add=True)
	utimestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username