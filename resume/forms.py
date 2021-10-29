from django import forms
from django.conf import settings

from django.forms import ModelForm
from django.forms import BaseModelFormSet
from django.forms import ModelFormSetFactory

from .models import Resume,WorkExperience,Education,Certification,Skill,Language,Interests

class WorkExperienceForm(ModelForm):
	#Mod
	class Meta:
		model = WorkExperience
		fields = ['position','employer','city','start_date','end_date','achievements']
		widgets = {'position':forms.TextInput(attrs={'class':'form-control'}),

					'employer':forms.TextInput(attrs={'class':'form-control'}),
				}