from django.test import TestCase
from .scoring import calculate_task_score
from datetime import date, timedelta

class ScoringAlgorithmTests(TestCase):
    
    def test_overdue_task_score(self):
        """Task due yesterday should have a huge score"""
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        task = {
            'due_date': yesterday,
            'importance': 5,
            'estimated_hours': 1
        }
        score = calculate_task_score(task)
        # Base (150) + Importance(5*5=25) + Effort(<2h=15) = 190 (approx)
        self.assertTrue(score > 100, "Overdue task should have very high score")

    def test_quick_win_bonus(self):
        """Short tasks should get a bonus"""
        future = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        
        long_task = {'due_date': future, 'importance': 5, 'estimated_hours': 10}
        short_task = {'due_date': future, 'importance': 5, 'estimated_hours': 1}
        
        score_long = calculate_task_score(long_task)
        score_short = calculate_task_score(short_task)
        
        self.assertTrue(score_short > score_long, "Short task should score higher than long task")

    def test_invalid_date_handling(self):
        """Should not crash if date is broken"""
        task = {
            'due_date': "not-a-date",
            'importance': 5,
            'estimated_hours': 1
        }
        try:
            calculate_task_score(task)
        except Exception:
            self.fail("Algorithm crashed on invalid date")