# ------------------------------------------------------------------------------
# Author: Saber Benafah - Computer Scientist
# Description: All views in this app were developed from scratch by me.
# ------------------------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, ArchiveForm, CustomUserForm
from .models import Archive, CustomUser
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'archive_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def home(request):
    return render(request, 'archive_app/home.html')

@login_required
def consultation(request):
    archives = Archive.objects.all()
    return render(request, 'archive_app/consultation.html', {'archives': archives})

# Archive config table
@login_required
def archive_config(request):
    # Only admins can access user management
    if request.user.role != 'Admin':
        messages.error(request, "Access denied: Admins only.")
        return redirect('home')
    
    users = CustomUser.objects.all()
    return render(request, 'archive_app/archive_config.html', {'users': users})
@login_required
def add_line(request):
    # Admins and Archivists can add lines
    if request.user.role not in ['Admin', 'Archivist']:
        messages.error(request, "Access denied: Insufficient permissions.")
        return redirect('home')

    if request.method == 'POST':
        form = ArchiveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Archive entry added successfully.")
            return redirect('consultation')
    else:
        form = ArchiveForm()
    return render(request, 'archive_app/add_line.html', {'form': form})


@login_required
def edit_line(request, id):
    # Admins and Archivists can edit lines
    if request.user.role not in ['Admin', 'Archivist']:
        messages.error(request, "Access denied: Insufficient permissions.")
        return redirect('home')

    archive = get_object_or_404(Archive, id=id)
    if request.method == 'POST':
        form = ArchiveForm(request.POST, instance=archive)
        if form.is_valid():
            form.save()
            messages.success(request, "Archive entry updated successfully.")
            return redirect('consultation')
    else:
        form = ArchiveForm(instance=archive)
    return render(request, 'archive_app/edit_line.html', {'form': form, 'archive': archive})

def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'

@login_required
def delete_line(request, id):
    if request.user.role not in ['Admin', 'Archivist']:
        messages.error(request, "Access denied: Insufficient permissions.")
        return redirect('consultation')
    
    archive = get_object_or_404(Archive, id=id)
    archive.delete()
    messages.success(request, "Archive entry deleted.")
    return redirect('consultation')

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = CustomUserForm()
    return render(request, 'archive_app/create_user.html', {'form': form})

@user_passes_test(is_admin)
def edit_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user_obj.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('home')
    else:
        form = CustomUserForm(instance=user_obj)
    return render(request, 'archive_app/edit_user.html', {'form': form, 'edit': True})

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_admin)
def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'archive_app/list_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.user == user:
        messages.error(request, "You cannot delete your own account.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('list_users')

import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Archive
from .forms import UploadCSVForm
from django.contrib import messages

# CSV upload view
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Archive.objects.create(
                    dossier_number=row['numero_dossier'],
                    colonne=row['colonne'],
                    etage=row['etage'],
                    rayon=row['rayon'],
                    site=row['site'],
                    nom_fournisseur=row['nom_fournisseur'],
                    contact=row['contact'],
                    fonction=row['fonction'],
                    mobile=row['mobile'],
                    tel_fixe=row['tel_fixe'],
                    email=row['email'],
                    domaine=row['domaine'],
                    specialite=row['specialite'],
                    provenance=row['provenance'],
                    observation=row['observation']
                )
            messages.success(request, 'CSV file imported successfully.')
            return redirect('consultation')
    else:
        form = UploadCSVForm()
    return render(request, 'archive_app/upload_csv.html', {'form': form})

# CSV download view
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archives.csv"'

    writer = csv.writer(response)
    writer.writerow(['numero_dossier', 'colonne', 'etage', 'rayon', 'site', 'nom_fournisseur', 'contact',
                     'fonction', 'mobile', 'tel_fixe', 'email', 'domaine', 'specialite', 'provenance', 'observation'])

    for archive in Archive.objects.all():
        writer.writerow([
            archive.dossier_number,
            archive.colonne,
            archive.etage,
            archive.rayon,
            archive.site,
            archive.nom_fournisseur,
            archive.contact,
            archive.fonction,
            archive.mobile,
            archive.tel_fixe,
            archive.email,
            archive.domaine,
            archive.specialite,
            archive.provenance,
            archive.observation
        ])

    return response
