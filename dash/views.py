from django import forms
from django.http import FileResponse, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm, SubmissionForm
from .models import JobPost, Submission
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Message
from .models import Submission
from .forms import MessageForm
from itertools import groupby
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.views.static import serve

@login_required
def reply_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, recipient=request.user)
    initial_data = {
        'subject': f"Re: {message.subject}",
        'recipient': message.sender,
    }
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(sender=request.user)
            message.sender = request.user
            message.save()
            messages.success(request, 'Your reply has been sent.')
            print(message_id)
            print(request.user)

            return redirect('/dashboard/inbox')

    else:
        form = MessageForm(initial=initial_data)
    print(message_id)
    print(request.user)

    return render(request, 'communication/send_message.html', {'form': form})




@login_required
def inbox(request):
    messages = Message.objects.filter(Q(recipient=request.user) | Q(sender=request.user))
    usernames = set()
    unique_messages = []
    for message in messages:
        if message.sender.username not in usernames:
            usernames.add(message.sender.username)
            unique_messages.append({'sender__username': message.sender.username})
    unread_count = Message.objects.filter(recipient=request.user, unread=True).count()
    return render(request, 'communication/inbox.html', {'messages': unique_messages, 'unread_count': unread_count})



@login_required
def user_messages(request, username):
    received_messages = Message.objects.filter(sender__username=username, recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user, recipient__username=username)
    messages = (received_messages | sent_messages).order_by('-sent_at')
    for message in messages:
        if message.recipient == request.user and not message.read_at:
            message.read_at = timezone.now()
            message.save()
    unread_count = Message.objects.filter(recipient=request.user, read_at=None).count()
    return render(request, 'communication/user_messages.html', {'messages': messages, 'username': username, 'unread_count': unread_count})








@login_required
def submissions(request):
    user = request.user
    submissions = Submission.objects.filter(job_post__user=user)
    success_message = messages.get_messages(request)
    return render(request, 'submissions.html', {'submissions': submissions, 'success_message': success_message})


@login_required
def send_message(request, submission_id, message_id=None):
    submission = get_object_or_404(Submission, pk=submission_id, job_post__user=request.user)
    parent_message = get_object_or_404(Message, pk=message_id, recipient=request.user) if message_id else None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(sender=request.user)
            message.sender = request.user
            message.recipient = User.objects.get(username=submission.user.username)  # set the recipient to the submission user
            message.parent_message = parent_message
            message.save()
            messages.success(request, 'Your message has been sent.')
            return redirect('submissions')
    else:
        initial_data = {'parent_message': parent_message} if parent_message else {'recipient': submission.user.username}
        form = MessageForm(initial=initial_data)

    form.fields['recipient'].widget = forms.HiddenInput()
    return render(request, 'communication/send_message.html', {'form': form, 'submission': submission, 'parent_message': parent_message, 'recipient': submission.user.username})




@login_required
def dashboard_view(request):
    username = request.user.username
    job_posts = JobPost.objects.filter(user=request.user)
    message_count = Message.objects.filter(recipient=request.user, unread=False).count()
    if request.method == 'POST':
        if 'post_job' in request.POST:
            form = JobPostForm(request.POST)
            if form.is_valid():
                job_post = form.save(commit=False)
                job_post.user = request.user
                job_post.save()
                return redirect('dashboard')
        elif 'delete_job' in request.POST:
            job_id = request.POST.get('delete_job')
            job_post = JobPost.objects.get(id=job_id, user=request.user)
            job_post.delete()
            return redirect('dashboard')
    else:
        form = JobPostForm()
    return render(request, 'auth/mdashboard.html', {'username': username, 'form': form, 'job_posts': job_posts, 'message_count': message_count})



@login_required
def job_dashboard_view(request):
    username = request.user.username
    job_posts = JobPost.objects.filter(user=request.user).order_by('-created_at')
    submission_count = Submission.objects.filter(job_post__user=request.user).count()
    
    if request.method == 'POST':
        if 'post_job' in request.POST:
            form = JobPostForm(request.POST)
            if form.is_valid():
                job_post = form.save(commit=False)
                job_post.user = request.user
                job_post.save()
                return redirect('dashboard')
        elif 'delete_job' in request.POST:
            job_id = request.POST.get('delete_job')
            job_post = JobPost.objects.get(id=job_id, user=request.user)
            job_post.delete()
            return redirect('dashboard')
    else:
        form = JobPostForm()
    
    return render(request, 'auth/joblistings.html', {'username': username, 'form': form, 'job_posts': job_posts, 'submission_count': submission_count})










def index(request):
    if request.method == 'POST' and 'delete_job' in request.POST:
        job_id = request.POST.get('delete_job')
        try:
            job_post = JobPost.objects.get(id=job_id)
            job_post.delete()
            messages.success(request, 'Job post deleted successfully.')
        except JobPost.DoesNotExist:
            messages.error(request, 'Job post not found.')
    
    job_posts = JobPost.objects.order_by('-created_at')
    paginator = Paginator(job_posts, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'auth/index.html', {'page_obj': page_obj})




@login_required
def edit_job(request, job_id):
    job_post = get_object_or_404(JobPost, id=job_id)

    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES, instance=job_post)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.created_at = timezone.now()  # Set created_at time to current time
            job_post.save()
            return redirect('/dashboard/all')
        else:
            print(form.errors)
    else:
        form = JobPostForm(instance=job_post)

    return render(request, 'edit_job.html', {'form': form})



def search_jobs(request):
    query = request.GET.get('q')
    if query:
        # Search for job posts that contain the query string in their title, description or company name.
        job_posts = JobPost.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(company__icontains=query)
        ).order_by('-created_at')
    else:
        job_posts = JobPost.objects.all().order_by('-created_at')
    
    return render(request, 'search_jobs.html', {'job_posts': job_posts})

#def job_detail(request, job_id):
 #   job_post = get_object_or_404(JobPost, id=job_id)
 #   return render(request, 'job_details.html', {'job_post': job_post})

@login_required
def job_detail(request, job_id):
    job_post = get_object_or_404(JobPost, pk=job_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.job_post = job_post
            submission.user = request.user
            submission.save()
            messages.success(request, 'Your resume has been submitted successfully.')
            return redirect('/dashboard/myapplications', pk=job_id)
    else:
        form = SubmissionForm()
    return render(request, 'sub.html', {'job_post': job_post, 'form': form})

"""
@login_required
def submissions(request):
    user = request.user
    submissions = Submission.objects.filter(job_post__user=user)
    return render(request, 'submissions.html', {'submissions': submissions})
"""

#@login_required
#def my_files(request):
#    submissions = Submission.objects.filter(user=request.user)
#    return render(request, 'my.html', {'submissions': submissions})

"""
@login_required
def my_files(request):
    submissions = Submission.objects.filter(user=request.user)
    
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
        submission.delete()
        messages.success(request, 'Your file has been deleted.')
        return redirect('my_files')
    
    return render(request, 'my.html', {'submissions': submissions})
"""
@login_required
def my_files(request):
    submissions = Submission.objects.filter(user=request.user)
    
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
        submission.delete()
        messages.success(request, 'Your file has been deleted.')
        return redirect('my_files')
    
    return render(request, 'my.html', {'submissions': submissions})


@login_required
def download_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    if submission.user != request.user:
        # Only the owner of the submission can download the file
        return HttpResponseNotFound()

    file_path = submission.resume.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(submission.resume.name)
    return response

@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    submission.delete()
    messages.success(request, 'Your file has been deleted.')
    return redirect('my_files')


"""" message """


#@login_required
#@user_passes_test(lambda user: user.is_authenticated)
#def protected_serve(request, path, document_root=None, show_indexes=False):
#    return serve(request, path, document_root, show_indexes)

@login_required
def download_resume(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    if submission.user != request.user:
        # Only the owner of the submission can download the file
        return HttpResponseNotFound()

    file_path = submission.resume.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(submission.resume.name)
    return response