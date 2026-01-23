from django.db import models

class Instituition(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=20, unique=True, null=False, blank=False)
    campus = models.CharField(max_length=50, null=False, blank=False)
    acronym = models.CharField(max_length=10, null=False, blank=False)
    image = models.ImageField(upload_to='institutions/photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.acronym} - {self.campus}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    institution = models.ForeignKey(Instituition, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} - {self.institution.acronym}"

class Project(models.Model):

    STATUS_CHOICES = [
        ('pending_approval', 'Aprovação Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
    ]

    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curso', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')

    members = models.ManyToManyField('auth.User', related_name='integrantes', blank=True)


    def __str__(self):
        return self.title
    
class ApprovalSolicitation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='approval_solicitations')
    message = models.TextField(null=False, blank=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='approval_solicitations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Solicitação de {self.user.username} para o projeto {self.project.title}"