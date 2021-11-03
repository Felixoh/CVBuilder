from django import forms
from django.conf import settings


### Custom User Creation Forms
from django import forms
from django.forms import TextInput
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.password_validation import validate_password

################# Vendor Forms ######################
from django.forms import ModelForm
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory
from tinymce.widgets import TinyMCE

from .models import Resume,WorkExperience,Education,Certification,Skill,Language,Interests,Profile

class ChooseForm(forms.Form):
	RESUME_CHOICES = (
	    ('jakarta', 'Jakarta'),
	    ('new_york', 'New York'),
	    ('tokyo', 'Tokyo'),
	    ('rome', 'Rome'),
	    ('sf', 'San Francisco'),
    )
	resume_template = forms.ChoiceField(choices=RESUME_CHOICES)


class MyModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(MyModelFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'user', 'id', ]
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'For example: Data Scientist or Sales Manager'}),
                   'user': forms.HiddenInput(),
                   'id': forms.HiddenInput(), }
        labels = {'name': 'Resume name'}


class WorkExperienceForm(ModelForm):
	#Modify how the data will be formatted in the  
	start_date = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                           widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))
	end_date = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS,
                         widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'date-picker', 'placeholder': 'DD/MM/YYYY'}))

	class Meta:
		model = WorkExperience
		fields = ['position','employer','city','start_date','end_date','achievements']
		widgets = {'achievements': TinyMCE(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'position': forms.TextInput(attrs={'placeholder': 'Example: Manager'}),
                   'company': TextInput(attrs={'placeholder': 'Example: KCB'}),
                   'city': TextInput(attrs={'placeholder': 'For example: Mombasa'}),
                   'resume': forms.HiddenInput(), }

WorkExperienceFormSet = modelformset_factory(WorkExperience, form=WorkExperienceForm, formset=MyModelFormSet, extra=1,max_num=5)


class EducationForm(ModelForm):
	class Meta:
		model = Education
		fields = ['school', 'degree', 'major', 'gpa', 'city', 'start_date', 'end_date', 'resume', ]
		widgets = {'school': forms.TextInput(attrs={'placeholder': 'Example: Kibabii University :','class':'form-control'}),
		       'degree': forms.TextInput(attrs={'class': 'form-control'}),
		       'major': forms.TextInput(attrs={'class': 'form-control'}),
		       'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
		       'city': forms.TextInput(attrs={'class': 'form-control'}),
		       'resume': forms.HiddenInput(),}

		labels = {'gpa': 'Grade'}
		

EducationFormSet = modelformset_factory(Education,form=EducationForm,formset=MyModelFormSet,max_num=3)


class SkillForm(ModelForm):
	def clean(self):
		cleaned_data = super(SkillForm,self).clean()
		name = cleaned_data.get('name')
		competency = cleaned_data.get('competency')
		if name and competency not in [1, 2, 3, 4, 5]:
			raise forms.ValidationError("Please select a competency level for your skill")

		if competency in [1, 2, 3, 4, 5] and not name:
			raise forms.ValidationError("Please enter a skill first")

	class Meta:
		model = Skill
		fields = ['name', 'competency', 'resume', ]
		widgets = {'competency': forms.Select(attrs={'class': 'form-control'}),
		           'name': forms.TextInput(attrs={'class': 'form-control'}),
		           'resume': forms.HiddenInput(),
		           }
		labels = {'name': 'Skill name'}

SkillFormSet = modelformset_factory(Skill,form=SkillForm,formset=MyModelFormSet,max_num=5)

class CertificationForm(ModelForm):
    date_obtained = forms.DateField(required=False,widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Certification
        fields = ['name', 'date_obtained', 'city', 'resume', ]
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Example : Certified Data Analyst','class':'form-control'}),
                   'city': forms.TextInput(attrs={'placeholder': 'Example: Nairobi ','class':'form-control'}),
                   'resume': forms.HiddenInput(), }

        labels = {'name': 'Certification Name'}


CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, formset=MyModelFormSet, max_num=5)

class LanguageForm(ModelForm):
	def clean(self):
		cleaned_data = super(LanguageForm,self).clean()
		name = cleaned_data.get('name')
		competency = cleaned_data.get('competency')

		if name and competency not in [1, 2, 3, 4, 5]:
			raise forms.ValidationError("Please select a competency level for your language")
		if competency in [1, 2, 3, 4, 5] and not name:
			raise forms.ValidationError("Please enter a language first")

	class Meta:
		model = Language
		fields = ['name', 'competency', 'resume', ]
		widgets = {'competency': forms.Select(attrs={'class': 'form-control'}),
		           'name': forms.TextInput(attrs={'class': 'form-control'}),
		           'resume': forms.HiddenInput(), }

		labels = {'name': 'Language name'}
LanguageFormSet = modelformset_factory(Language, form=LanguageForm, formset=MyModelFormSet, max_num=5)




class CustomUserCreationForm(UserCreationForm): 
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 8:
            raise forms.ValidationError("Your username is too short. A username must be at least 8 characters long")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Your username is already taken")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if validate_password(password1):
            raise forms.ValidationError('This password is not valid please give a more secure password')
        return password1

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match. Please try again")
        return super(UserCreationForm, self).clean(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', )
        widgets = {'first_name': TextInput(attrs={'placeholder': 'What is your first name?'}),
                   'last_name': TextInput(attrs={'placeholder': 'What is your last name?'}), }

### Profile Updating Form
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['job_title', 'address', 'address2', 'city', 'country', 'phone_number', 'linked_in', 'objective',
                  'profile_pic', ]
        widgets = {'job_title': TextInput(attrs={'placeholder': 'Desired job title?'}),
                   'address': TextInput(attrs={'placeholder': 'Home street address?'}),
                   'address2': TextInput(attrs={'placeholder': 'Sub-County '}),
                   'city': TextInput(attrs={'placeholder': 'What city do you live in?'}),
                   'phone_number': TextInput(attrs={'placeholder': 'What is your mobile number?', }),
                   'linked_in': TextInput(attrs={'placeholder': 'What is your Social Media profile?'}), }
        labels = {"linked_in": "LinkedIn profile",
                  "phone_number": "Mobile number",
                  "profile_pic": "Profile picture",
                  "objective": "Career objective",
                  "address2": "Address",}