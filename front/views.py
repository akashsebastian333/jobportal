from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render
from dash.models import JobPost



#def index(request):
#   return render(request,'index2.html')


#def indexpage(request):
#    jobs = JobPost.objects.order_by('-created_at')[:6]  # slice the queryset to get only the first 6 jobs
#    context = {'jobs': jobs}
#    return render(request, 'index.html', context)

def indexpage(request):
    jobs = JobPost.objects.order_by('-created_at')[:6]  # slice the queryset to get only the first 6 jobs
    context = {'jobs': jobs}
    return render(request, 'index.html', context)

def job_list(request):
    jobs = JobPost.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs.html', context)