from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ----------- Custom User Manager ----------- #
class CustomUserManager(BaseUserManager):
    def create_user(self, username, branch, role, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, branch=branch, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, branch, password):
        user = self.create_user(username=username, branch=branch, role='Admin', password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# ----------- Custom User Model ----------- #
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    
    username = models.CharField(max_length=50, unique=True)
    branch = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['branch']

    def __str__(self):
        return self.username

# ----------- Archive Model ----------- #
class Archive(models.Model):
    dossier_number = models.CharField(max_length=20, verbose_name="N° Dossier")
    colonne = models.CharField(max_length=20)
    etage = models.CharField(max_length=20)
    rayon = models.CharField(max_length=20)
    site = models.CharField(max_length=50)
    nom_fournisseur = models.CharField(max_length=100)
    #fournisseur_site = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    tel_fixe = models.CharField(max_length=20)
    email = models.EmailField()
    domaine = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    provenance = models.CharField(max_length=100)
    observation = models.TextField(blank=True)

    def __str__(self):
        return f"Dossier {self.dossier_number}"
