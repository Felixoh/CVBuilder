from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resume(models.Model):
	name = models.CharField(max_length=255,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,editable=False)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)

	def __str__(self):
		return self.name

class WorkExperience(models.Model):
	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	position = models.CharField(max_length=255,blank=True)
	employer = models.CharField(max_length=255,blank=True)
	city = models.CharField(max_length=255,blank=True)
	start_date = models.DateField(null=True,blank=True)
	end_date = models.DateTimeField(null=True,blank=True)
	achievements = models.TextField(blank=True)

	def __str__(self):
		return self.position

class Education(models.Model):
	DEGREE_CHOICES = (
		("JD","Junior Degree"),
		("MD","Masters Degree"),
		("PHD","Doctorate"),
		)

	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	school_name = models.CharField(max_length=255,blank=True)
	degree = models.CharField(max_length=255,choices=DEGREE_CHOICES,blank=True)

	def __str__(self):
		return self.name

class Certification(models.Model):
	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	date_obtained = models.DateField(null=True,blank=True)
	city = models.CharField(max_length=255,blank=True)

class Skill(models.Model):
	COMPETENCY = (
		(1,'Below Average'),
		(2,'Average'),
		(3,'Good'),
		(4,'Excellent'),
		)

	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=255)
	competency = models.IntegerField(choices=COMPETENCY,null=True,blank=True)

	def __str__(self):
		return self.name

class Language(models.Model):
	LANGUAGE_COMPETENCE = (
		(1,'Beginner Level'),
		(2,'Conversational'),
		(3,'Business Level'),
		(4,'Fluent Level'),
		)

	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=255,blank=True)
	competency = models.IntegerField(choices=LANGUAGE_COMPETENCE,null=True,blank=True)

	def __str__(self):
		return self.name

class Interests(models.Model):
	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=255,blank=True)

	def __str__(self):
		return self.name
