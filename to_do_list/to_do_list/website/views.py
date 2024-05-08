from django.shortcuts import render, redirect
from .models import Note, NoteUser
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorator import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group 
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, never_cache
from ipware import get_client_ip
from django.utils import timezone

def custom_404(request, exception):
    return redirect('home')

def home(request):
    return render(request, "base.html")

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['noteuser'])
# def homepage(request, pk):
#     user = NoteUser.objects.get(id=pk)
#     form = NoteForm()

#     if request.method == 'POST':
#         if user:
#             form = NoteForm(request.POST)
#             if form.is_valid():
#                 new_note = form.save()
#                 new_note.user = user  # Assign the user before saving
#                 new_note.save()
#                 messages.success(request, 'Note added successfully')
#                 form = NoteForm()
#         else:
#             form = NoteForm()
#             return render(request, "home.html", context={"notes": [], "form": form})
#     user_notes = user.note_set.all()  # Use note_set to get all notes for the user

#     return render(request, "home.html", context={"notes": user_notes, "form": form})
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['noteuser', 'admin'])
# def homepage(request, pk):
#     user = NoteUser.objects.get(id=pk)
#     form = NoteForm()

#     if request.user.groups.first().name == 'noteuser':
#         if request.method == 'POST':
#             form = NoteForm(request.POST)
#             if form.is_valid():
#                 new_note = form.save(commit=False)
#                 new_note.user = user
#                 new_note.save()
#                 messages.success(request, 'Note added successfully')
#                 form = NoteForm()

#         user_notes = user.note_set.all()
#         return render(request, "home.html", context={"notes": user_notes, "form": form})
#     elif request.user.is_staff:
#         return render(request, "adminhome.html", context={})
#     else:
#         return render(request, "home.html", context={"notes": user_notes, "form": NoteForm()})
@login_required(login_url='login')
@allowed_users(allowed_roles=['noteuser'])
@never_cache
def homepage(request, pk):
    if pk != request.session['user_id']:
        pk = request.session['user_id']
    user = NoteUser.objects.get(id=pk)
    # user = get_object_or_404(NoteUser, id=pk)
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = user
            new_note.save()
            messages.success(request, 'Note added successfully')
            form = NoteForm()

    user_notes = user.note_set.all()
    return render(request, "home.html", context={"notes": user_notes, "form": form})
   

@unauthenticated_user
@never_cache
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Avoid printing sensitive information like passwords
        # print(f"Username: {username}")

        user = authenticate(request, username=username, password=password)
        # print(f"Authenticated User: {user}")
        
        if user is not None:
            login(request, user)
            userId = request.user.id
            request.session['username'] = f"{username}"
            
            if user.is_staff:
                messages.success(request, 'Logged in successfully as Admin')
                return redirect('admin_homepage', userId)  # Redirect to admin homepage
            else:
                note_user = NoteUser.objects.get(user=user)
                NoteuserId = note_user.id
                request.session['user_id'] = note_user.id
                messages.success(request, 'Logged in successfully')
                return redirect('homepage', NoteuserId)

        else:
            messages.error(request, 'Email or password is incorrect')
            print("Authentication failed")

    return render(request, template_name='login.html')

# @unauthenticated_user
# def loginuser(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # Avoid printing sensitive information like passwords
#         # print(f"Username: {username}")

#         user = authenticate(request, username=username, password=password)
#         # print(f"Authenticated User: {user}")
        
#         if user is not None:
#             login(request, user)
#             userId = request.user.id
#             request.session['username'] = f"{username}"

#             if user.is_staff:
#                 messages.success(request, 'Logged in successfully as Admin')
#                 return redirect('admin_homepage', userId)  # Redirect to admin homepage
#             else:
#                 note_user = NoteUser.objects.get(user=user)
#                 userId = note_user.id
#                 note_user.login_attempts = 0
#                 note_user.blocked_ip_address = None # add this new line
#                 note_user.blocked_until = None 
#                 note_user.save()
#                 messages.success(request, 'Logged in successfully')
#                 return redirect('homepage', userId)

#         else:
#             if note_user := NoteUser.objects.filter(user__username=username).first():
#                 note_user.login_attempts += 1
#                 note_user.last_login_attempt = timezone.now()
                
#                 if note_user.login_attempts >= 5:
#                     note_user.blocked_until = timezone.now() + timezone.timedelta(minutes=15)
#                     note_user.save()
#                     messages.error(request, "Too many unsuccessful login attempts. Your account is blocked for 15 minutes.")
#                     return redirect('login')

#                 note_user.save()
#                 messages.error(request, 'Email or password is incorrect')
#                 print("Authentication failed")

#     return render(request, template_name='login.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminhomepage(request, pk):
    # Fetch all users
    users = NoteUser.objects.all()

    # Create a list to store user data for rendering in the template
    user_data = []

    # Iterate through each user to fetch their posts
    for user in users:
        user_posts = Note.objects.filter(user=user)
        user_data.append({
            'user': user,
            'posts': user_posts,
        })

    return render(request, "adminhome.html", context={'user_data': user_data})

# @unauthenticated_user
# def registeruser(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
            
#             # Create a NoteUser associated with the created user
#             NoteUser.objects.create(user=user, name=form.cleaned_data['username'], email=form.cleaned_data['email'])
            
#             messages.success(request, 'User is added successfully')
#             return redirect('login')
#     return render(request, "sign_up.html", context={"form": form})

@unauthenticated_user
def registeruser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # user = form.save()
            user = form.save(commit=False)
            user.save()
            
            # Check if the 'noteuser' group exists, and create it if not
            # noteuser_group, created = Group.objects.get_or_create(name='noteuser')

            # Add the user to the 'noteuser' group
            # user.groups.add(noteuser_group)

            # Create a NoteUser associated with the created user
            # NoteUser.objects.create(user=user, name=form.cleaned_data['username'], email=form.cleaned_data['email'])

            messages.success(request, 'User is added successfully')
            return redirect('login')

    return render(request, "sign_up.html", context={"form": form})

def logoutUser(request):
    logout(request)
    return redirect('login')


def delete_note(request, note_id):
    note = Note.objects.get(id=note_id) 
    user_id = note.user.id
    print(note, " ", user_id)
    note.delete()
    messages.success(request, 'Note deleted successfully')
    return redirect('homepage', pk=user_id)