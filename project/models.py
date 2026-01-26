from django.db import models
from ckeditor.fields import RichTextField

class Institution(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=20, unique=True, null=False, blank=False)
    campus = models.CharField(max_length=50, null=False, blank=False)
    acronym = models.CharField(max_length=10, null=False, blank=False)
    image = models.ImageField(upload_to='institutions/photos/', null=True, blank=True)


    def __str__(self):
        return f"{self.acronym} - {self.campus}"

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

class Course(models.Model):
    name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.name} - {self.institution.acronym}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

def project_image_path(instance, filename):
    return f'projects/{instance.id}/images/{filename}'

class Project(models.Model):

    STATUS_CHOICES = [
        ('pending_approval', 'Pendente de Aprovação'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
    ]

    TYPE_CHOICES = [
        ('research', 'Pesquisa e Desenvolvimento'),
        ('integrator', 'Projeto Integrador'),
        ('thesis', 'Tese de Conclusão de Curso'),
    ]

    title = models.CharField(max_length=200, null=False, blank=False)
    banner = models.ImageField(upload_to='projects/banners/', null=True, blank=True)
    description = RichTextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses', null=False, blank=False) # só foi alterado para true para testar a criação de projetos sem curso, mudar para false antes de fazer commit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    is_private = models.BooleanField(default=False)
    image = models.ImageField(upload_to=project_image_path, null=True, blank=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='research')

    members = models.ManyToManyField('authentication.User', related_name='members', blank=True)
    orientators = models.ManyToManyField('authentication.User', related_name='orientators', blank=True)
    
    link_github = models.URLField(null=True, blank=True)
    link_youtube = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

class ApprovalSolicitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='approval_solicitations')
    message = models.TextField(null=False, blank=False)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='approval_solicitations')
    created_at = models.DateTimeField(auto_now_add=True)
    # is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Solicitação de {self.user.username} para criação do projeto {self.project.title}"

    class Meta:
        verbose_name = "Solicitação de aprovação"
        verbose_name_plural = "Solicitações de aprovação"


class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=False, blank=False)
    likes = models.ManyToManyField('authentication.User', related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user.username} no projeto {self.project.title}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"


class ReportProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Denuncia de {self.user.username} sobre o projeto {self.project.title}"

    class Meta:
        verbose_name = "Denúncia de projeto"
        verbose_name_plural = "Denúncias de projetos"


class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='comment_reports')
    reason = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Denuncia de {self.user.username} sobre comentário {self.comment.id}"

    class Meta:
        verbose_name = "Denúncia de comentário"
        verbose_name_plural = "Denúncias de comentários"
