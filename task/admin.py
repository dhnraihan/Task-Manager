from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'due_date', 'user' )
    last_fillter = ('title', 'user')
    search_fields = ('title', 'description')

