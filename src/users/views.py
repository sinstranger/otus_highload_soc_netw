import json

import psycopg2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


from users.custom_db import create_user, get_user, check_password, search_users


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


@csrf_exempt
@require_GET
def search_users_view(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')

    if not first_name or not last_name:
        return JsonResponse({"error": "first_name and last_name are required"}, status=400)

    try:
        results = search_users(first_name, last_name)
        users = []
        for row in results:
            users.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "birthdate": str(row[3]),
                "gender": row[4],
                "interests": row[5],
                "city": row[6],
            })
        return JsonResponse(users, safe=False, status=200)

    except psycopg2.OperationalError:
        return JsonResponse({"error": "Service temporarily unavailable"}, status=503)

    # except Exception as e:
    #     print(e)
    #     return JsonResponse({"error": str(e)}, status=500)
