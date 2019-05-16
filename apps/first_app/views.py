from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from time import strftime
from datetime import date
import bcrypt


import re  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, 'first_app/index.html')

def register_form(request):
    return render(request, 'first_app/index.html')

def register_user(request):
    errors = {}
    if len(request.POST['first_name'])<2:
        errors['first_name'] = "First name must be at least 2 characters long"
    if request.POST['first_name'].isalpha() == False:
        errors['first_name'] = "First name must have only letters"
    if len(request.POST['last_name'])<2:
        errors['last_name'] = "Last name must be at least 2 characters long"
    if request.POST['last_name'].isalpha() == False:
        errors['last_name'] = "Last name must have only letters"
    users_with_email = User.objects.filter(email=request.POST['email'])
    if len(users_with_email) > 0:
        errors['email'] = "Email is taken"
    if not EMAIL_REGEX.match(request.POST['email']):
        errors['email'] = "Email is invalid"
    if len(request.POST['password']) < 8:
        errors['password'] = "Password must be at least 8 characters long"
    if request.POST['password'] != request.POST['confirm_password']:
        errors['password'] = "Password must be the same as confirmation"
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=hash1)
        print('*'* 50)
        print('created a new user', new_user.__dict__)
        return redirect('/')

def login_user(request):
    users_with_email = User.objects.filter(email=request.POST['email'])
    if len(users_with_email) > 0:
        found_user = users_with_email[0]
        result = bcrypt.checkpw(request.POST['password'].encode(),found_user.password.encode())
        if result == True:
            request.session['user_id'] = found_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid login information")
            return redirect('/')
    else:
        messages.error(request,"Invalid login information")
        return redirect('/')

def dashboard(request):
    all_jobs = Job.objects.all()
    current_user = User.objects.get(id=request.session['user_id'])

    context ={
        "jobs" : all_jobs,
         "curr_user": current_user
    }
    return render(request,'first_app/dashboard.html',context)

def new_job(request):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        "curr_user": current_user
    }
    return render(request,'first_app/new_job.html',context)

def create_job(request):
    current_user = User.objects.get(id=request.session['user_id'])
    errors = {}
    if len(request.POST['title'])<3:
        errors['title'] = "Title must be at least 3 characters long"
    if len(request.POST['description'])<3:
        errors['description'] = "Description must be at least 3 characters long"
    if len(request.POST['location'])<3:
        errors['location'] = "Location must be at least 3 characters long"
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/jobs/new')
    else:
        Job.objects.create(title=request.POST['title'],description=request.POST['description'],location=request.POST['location'],user=current_user)
        return redirect('/dashboard')

def job_details(request,id):
    current_job = Job.objects.get(id=id)
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        "curr_job": current_job,
        "curr_user": current_user
    }
    return render(request,'first_app/job_details.html',context)

def delete(request, id):
    current_job = Job.objects.get(id=id)
    current_job.delete()
    return redirect ('/dashboard')

def edit_job(request,id):
    current_job = Job.objects.get(id=id)
    current_user = User.objects.get(id=request.session['user_id'])
    context ={
        "curr_job":current_job,
        "curr_user": current_user
    }
    return render(request,'first_app/edit.html',context)

def update(request,id):
    current_job = Job.objects.get(id=id)
    errors = {}
    if len(request.POST['title'])<3:
        errors['title'] = "Title must be at least 3 characters long"
    if len(request.POST['description'])<3:
        errors['description'] = "Description must be at least 3 characters long"
    if len(request.POST['location'])<3:
        errors['location'] = "Location must be at least 3 characters long"
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/jobs/edit/'+str(id))
    else:
        current_job.title = request.POST['title']
        current_job.description = request.POST['description']
        current_job.location = request.POST['location']
        current_job.save()
    return redirect('/dashboard')

def logout(request):
    return redirect('/')

