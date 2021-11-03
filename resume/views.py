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

FORM_TYPES = ('work_experience', 'certifications', 'education', 'skills', 'languages')

from .models import Resume, WorkExperience, Certification, Education, Skill, Language
from .forms import ChooseForm ,CustomUserCreationForm,CustomUserChangeForm,ProfileUpdateForm
from .forms import (ResumeForm, WorkExperienceFormSet, CertificationFormSet,
                    EducationFormSet, SkillFormSet, LanguageFormSet)

FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceFormSet),
         ('certifications', CertificationFormSet),
         ('education', EducationFormSet),
         ('skills', SkillFormSet),
         ('languages', LanguageFormSet),]


# Views logic with Protected access Functionalities
def base(request):

	return render(request,'resume/base.html')

@login_required(login_url='login')
def home(request):

	return render(request,'resume/layout.html')

@login_required
def choose(request,pk):
	user = request.user
	pp_url = user.profile.profile_pic.url.strip('/')
	resume = Resume.objects.get(pk=pk)
	form = ChooseForm(request.POST)

	if request.method == 'GET':
		form = ChooseForm()
	elif request.method == 'POST' and 'view-resume' in request.POST:
		if form.is_valid() and form.cleaned_data['resume_template'] == 'rome':
			return render(request, 'resume/rome.html', {'form': form, 'resume': resume, 'pp_url': pp_url})

	return render(request, 'resume/choose.html', {'form': form, 'resume': resume})


@login_required
def my_resumes(request):
    user = request.user
    resumes = Resume.objects.filter(user=user).order_by('-created_at')
    return render(request, 'resume/my_resume.html', {'resumes': resumes})

def dict_has_data(input_dict):
    has_data = False
    for key in input_dict:
        if input_dict[key]:
            has_data = True
            break
    return has_data

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
        	#Do some action before saving the user to the database
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def delete_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    resume.delete()
    messages.success(request, "Your resume has been deleted!")
    return HttpResponseRedirect(reverse('my-resumes'))

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been saved!')
            return HttpResponseRedirect(reverse('edit-profile'))
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'p_form': p_form,
               'u_form': u_form,
               }
    return render(request, 'resume/profile.html', context)

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

	def done(self, form_list, **kwargs):
		user = self.request.user
		resume_form_data = self.get_cleaned_data_for_step('resumes')
		resume_name = resume_form_data['name']
		if 'pk' in self.kwargs:
		    pk = self.kwargs['pk']
		else:
		    pk = None

		resume, created = Resume.objects.update_or_create(id=pk, defaults={'user': user,
		                                                                   'name': resume_name, })

		for form_name in FORM_TYPES:
		    form_data_list = self.get_cleaned_data_for_step(form_name)
		    for form_data in form_data_list:
		        if not dict_has_data(form_data):
		            continue
		        form_data['resume'] = resume

		        form_instance = self.get_form(step=form_name)
		        obj = form_data.pop('id')
		        if obj:
		            form_instance.model.objects.filter(id=obj.id).update(**form_data)
		        else:
		            form_instance.model.objects.create(**form_data)

		messages.add_message(self.request, messages.SUCCESS, 'Resume has been saved!')

		return HttpResponseRedirect(reverse('my-resumes'))