from django.db import models
from django.conf import settings

#from django.contrib.auth.models import User //Invalid For now

############### User Data  #############
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django_resized import ResizedImageField

################# Resume Models + User Accounts Management  ##################
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Resume(models.Model):
	name = models.CharField(max_length=255,blank=True)
	created_at = models.DateTimeField(auto_now_add=True,editable=False)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True)

	def __str__(self):
		return self.name

class WorkExperience(models.Model):
	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	position = models.CharField(max_length=255,blank=True)
	employer = models.CharField(max_length=255,blank=True)
	city = models.CharField(max_length=255,blank=True)
	start_date = models.DateField(null=True,blank=True)
	end_date = models.DateField(null=True,blank=True)
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
	school = models.CharField(max_length=255,blank=True)
	degree = models.CharField(max_length=255,blank=True)
	major = models.CharField(max_length=255, blank=True)
	gpa = models.FloatField(null=True, blank=True)
	city = models.CharField(max_length=255, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.school

class Certification(models.Model):
	resume = models.ForeignKey(Resume,on_delete=models.CASCADE,blank=True)
	name = models.CharField(max_length=255,blank=True)
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

########## User Management Models ################################
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Select country)', blank=True)
    linked_in = models.CharField(max_length=255, blank=True)
    objective = HTMLField(blank=True)
    profile_pic = ResizedImageField(size=[250, 250], quality=100, default="profile-pics/default.jpg", upload_to="profile-pics")
    sub_expires_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    package = models.CharField(max_length=255)
    total = models.IntegerField()
    paid_status = models.BooleanField(default=False)

    def __str__(self):
        return self.package