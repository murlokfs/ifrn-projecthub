from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, username, password, **extra_fields)


def user_avatar_path(instance, filename):
    return f'avatars/{instance.id}/{filename}'

class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('student', 'Discente'),
        ('teacher', 'Docente'),
        ('visitor', 'Visitante'),
        ('admin', 'Administrador'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    email_institucional = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    registration = models.CharField(max_length=50, unique=True, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    course = models.ForeignKey('project.Course', on_delete=models.SET_NULL, null=True, blank=True)
    institution = models.ForeignKey('project.Instituition', on_delete=models.SET_NULL, null=True, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='visitor')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"



