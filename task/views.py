from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def home(request):
    # Get task statistics
    total_tasks = Task.objects.filter(user=request.user).count()
    pending_tasks = Task.objects.filter(user=request.user, status='pending').count()
    in_progress_tasks = Task.objects.filter(user=request.user, status='in_progress').count()
    completed_tasks = Task.objects.filter(user=request.user, status='completed').count()
    
    # Get recent tasks (top 5)
    recent_tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get upcoming tasks (due date is in the future and not completed)
    from django.utils import timezone
    upcoming_tasks = Task.objects.filter(
        user=request.user, 
        due_date__gt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).order_by('due_date')[:5]
    
    context = {
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'recent_tasks': recent_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'tasks/home.html', context)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})