import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .custom_db import create_user, get_user, check_password


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = create_user(data)
        return JsonResponse({'id': user_id})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = check_password(data['first_name'], data['password'])
        if user_id:
            return JsonResponse({'id': user_id})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


def get_user_view(request, user_id):
    user = get_user(user_id)
    if user:
        return JsonResponse(user)
    return JsonResponse({'error': 'Not found'}, status=404)
