from django.db import models
from authentication.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('Pesquisa', 'PESQUISA'),
        ('Integrador', 'INTEGRADOR'),
        ('TCC', 'TCC'),
    ]

    STATUS_CHOICES = [
        ('Aprovado', 'Aprovado'),
        ('Pendente', 'Pendente'),
        ('Reprovado', 'Reprovado'),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)

    description = RichTextUploadingField()

    guiding_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='guided_projects', 
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, related_name='projects')
    members = models.ManyToManyField(
        User,
        related_name='projects',
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Isso impede que o mesmo usuário curta o mesmo projeto mais de uma vez
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user} curtiu {self.project.title}"