from django.contrib import admin
from .models import Project, Campus, Course, Tag, ApprovalSolicitation, Comment, ReportProject, ReportComment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'status', 'type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'type', 'course', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

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
    list_display = ('project', 'user', 'reason_short', 'is_resolved', 'created_at')
    search_fields = ('project__title', 'user__full_name', 'reason')
    list_filter = ('is_resolved', 'created_at')
    readonly_fields = ('created_at', 'project', 'user', 'reason')
    actions = ['mark_as_resolved', 'mark_as_unresolved']
    
    def reason_short(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_short.short_description = 'Motivo'
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = 'Marcar como resolvido'
    
    def mark_as_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
    mark_as_unresolved.short_description = 'Marcar como não resolvido'

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

