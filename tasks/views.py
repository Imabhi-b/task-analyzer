import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score

@csrf_exempt
def analyze_tasks(request):
    if request.method == 'POST':
        try:
            # 1. Get data from the frontend
            data = json.loads(request.body)
            tasks = data if isinstance(data, list) else []

            # 2. Apply the "Brain" (Scoring algorithm)
            analyzed_tasks = []
            for task in tasks:
                score = calculate_task_score(task)
                task['score'] = score
                analyzed_tasks.append(task)

            # 3. Sort by Score (Descending order: Highest score first)
            analyzed_tasks.sort(key=lambda x: x['score'], reverse=True)

            # 4. Return results
            return JsonResponse(analyzed_tasks, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# ... keep your existing imports and analyze_tasks function ...

@csrf_exempt
def suggest_tasks(request):
    """
    Returns the top 3 tasks with a text explanation.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks = data if isinstance(data, list) else []

            # 1. Score them
            scored_tasks = []
            for task in tasks:
                score = calculate_task_score(task)
                
                # generate a simple explanation based on score
                explanation = "Standard priority task."
                if score > 100:
                    explanation = "CRITICAL: This task is overdue!"
                elif score > 50:
                    explanation = "High priority due to approaching deadline."
                elif task.get('estimated_hours', 0) < 2:
                    explanation = "Quick Win: Easy to complete."
                
                task['score'] = score
                task['explanation'] = explanation
                scored_tasks.append(task)

            # 2. Sort and slice top 3
            scored_tasks.sort(key=lambda x: x['score'], reverse=True)
            top_3 = scored_tasks[:3]

            return JsonResponse(top_3, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
    return JsonResponse({'error': 'POST method required'}, status=405)