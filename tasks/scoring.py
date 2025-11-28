from datetime import date, datetime

def calculate_task_score(task_data):
    """
    Calculates priority. Higher score = Higher priority.
    """
    score = 0
    today = date.today()

    # 1. Parse the date (Handle potential string format issues)
    try:
        # Assuming format YYYY-MM-DD coming from JSON
        due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # Fallback if date is invalid: Treat as due today
        due_date = today

    # 2. Urgency Calculation
    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 150  # CRITICAL: Overdue
    elif days_until_due == 0:
        score += 100  # Due today
    elif days_until_due <= 3:
        score += 50   # Due very soon
    elif days_until_due > 14:
        score -= 10   # Can wait

    # 3. Importance Weighting (Multiplier)
    # We multiply importance (1-10) by 5 to make it impactful
    importance = task_data.get('importance', 5) # Default to 5 if missing
    score += (importance * 5)

    # 4. Effort (Quick Wins Strategy)
    # If a task takes less than 2 hours, we give it a boost to clear it quickly
    hours = task_data.get('estimated_hours', 1)
    if hours < 2:
        score += 15
    elif hours > 8:
        score -= 5 # Big tasks feel heavier, slightly deprioritize (optional philosophy)

    # 5. Dependency Handling
    # If this task has dependencies (it waits on others), it might have lower immediate priority
    # OR, if others depend on THIS task, it needs higher priority.
    # For this assignment, let's say if it has dependencies, subtract score (blocked)
    deps = task_data.get('dependencies', [])
    if len(deps) > 0:
        score -= 20 

    return score