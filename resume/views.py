from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from django.views import View

from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

TEMPLATES = {'resumes': 'resume/resume.html',
             'work_experience': 'resume/work_experience.html',
             'certifications': 'resume/certifications.html',
             'education': 'resume/education.html',
             'skills': 'resume/skills.html',
             'languages': 'resume/languages.html',}

from .models import Resume, WorkExperience, Certification, Education, Skill, Language
from .forms import ChooseForm ,CustomUserCreationForm
from .forms import (ResumeForm, WorkExperienceFormSet, CertificationFormSet,
                    EducationFormSet, SkillFormSet, LanguageFormSet)

FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceFormSet),
         ('certifications', CertificationFormSet),
         ('education', EducationFormSet),
         ('skills', SkillFormSet),
         ('languages', LanguageFormSet),]


# Create your views here.
def home(request):

	return render(request,'resume/my_resume.html')

def my_resumes(request):
    user = request.user
    resumes = Resume.objects.filter(user=user).order_by('-created_at')
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class ResumeWizard(LoginRequiredMixin,SessionWizardView):
	login_url = '/login/'

	def get_form_initial(self,step):
		if 'pk' in self.kwargs:
			return {}
		return self.initial_dict.get(step, {})

	def get_form_instance(self, step):
		if 'pk' in self.kwargs:
		    pk = self.kwargs['pk']
		    resume = Resume.objects.get(id=pk)

		    if step == 'resumes':
		        return resume

		    if step == 'work_experience':
		        return resume.workexperience_set.all()

		    if step == 'certifications':
		        return resume.certification_set.all()

		    if step == 'education':
		        return resume.education_set.all()

		    if step == 'skills':
		        return resume.skill_set.all()

		    if step == 'languages':
		        return resume.language_set.all()
		else:
		    if step == 'resumes':
		        return None

		    if step == 'work_experience':
		        return WorkExperience.objects.none()

		    if step == 'certifications':
		        return Certification.objects.none()

		    if step == 'education':
		        return Education.objects.none()

		    if step == 'skills':
		        return Skill.objects.none()

		    if step == 'languages':
		        return Language.objects.none()
		return None

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

