from django.contrib import admin
from .models import Project, Campus, Course, Tag, ApprovalSolicitation, Comment, ReportProject, ReportComment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'status', 'type', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'type', 'course')

class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'cnpj')
    search_fields = ('name', 'acronym', 'cnpj')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')
    search_fields = ('name',)
    list_filter = ('campus',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ApprovalSolicitationAdmin(admin.ModelAdmin):
    list_display = ('project', 'user')
    search_fields = ('project__title', 'user__full_name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
    search_fields = ('project__title', 'user__full_name', 'content')

class ReportProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
    search_fields = ('project__title', 'user__full_name', 'reason', 'is_resolved')

class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'created_at')
    search_fields = ('comment__content', 'user__full_name', 'reason', 'is_resolved')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ApprovalSolicitation, ApprovalSolicitationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReportProject, ReportProjectAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)

