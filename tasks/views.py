from django.http import JsonResponse
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@csrf_exempt
def list_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().values()
        return JsonResponse(list(tasks), safe=False)

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            task = Task.objects.create(
                title=data['title'],
                description=data.get('description', ''),
                due_date=data.get('due_date', None),
                completed=False,
                assigned_to_id=data['assigned_to']
            )
            return JsonResponse({'message': 'Task created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def update_task(request, task_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            task = Task.objects.get(id=task_id)
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.due_date = data.get('due_date', task.due_date)
            task.completed = data.get('completed', task.completed)
            task.assigned_to_id = data.get('assigned_to', task.assigned_to_id)
            task.save()
            return JsonResponse({'message': 'Task updated successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'message': 'Task deleted successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(login_required, name='dispatch')
def get_task(request, task_id):
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': str(task.due_date) if task.due_date else None,
                'completed': task.completed,
                'assigned_to': task.assigned_to.username
            })
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def search_tasks(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        tasks = Task.objects.filter(title__icontains=query).values()
        return JsonResponse(list(tasks), safe=False)
@csrf_exempt
def assign_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            task = Task.objects.get(id=task_id)
            task.assigned_to_id = data['assigned_to']
            task.save()
            return JsonResponse({'message': 'Task assigned successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def complete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = True
            task.save()
            return JsonResponse({'message': 'Task marked as completed'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def uncomplete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = False
            task.save()
            return JsonResponse({'message': 'Task marked as uncompleted'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def get_user_tasks(request, user_id):
    if request.method == 'GET':
        tasks = Task.objects.filter(assigned_to_id=user_id).values()
        return JsonResponse(list(tasks), safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def get_task_comments(request, task_id):
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
            comments = task.comments.all().values('id', 'user__username', 'comment', 'created_at')
            return JsonResponse(list(comments), safe=False)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        