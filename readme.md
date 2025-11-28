# Smart Task Analyzer

A Python (Django) and JavaScript application that intelligently prioritizes tasks based on urgency, importance, and effort.

## How to Run

1. **Backend Setup:**
   ```bash
   cd task-analyzer
   python -m venv venv
   source venv/bin/activate  # (Or venv\Scripts\activate on Windows)
   pip install -r requirements.txt
   python manage.py runserver

## 🚀 Frontend Setup
Open the following file in any modern web browser:

```
frontend/index.html
```

---

# ⚙️ The Algorithm (Design Decisions)

The core scoring logic (located in `tasks/scoring.py`) assigns each task a **priority score** using a weighted formula.  
This ensures tasks are ranked in a **smart, meaningful, and actionable** way.

---

## 🏆 Priority Scoring Breakdown

### **1. Urgency (Highest Weight)**

| Condition | Score Impact |
|----------|--------------|
| **Overdue tasks** | **+150** |
| **Due within 3 days** | **+50** |

Urgency is heavily weighted to avoid missed deadlines and negative consequences.

---

### **2. Importance**

| Factor | Score Impact |
|--------|--------------|
| User-defined importance (1–10) | importance × **5** |

This ensures important tasks rise in priority without overshadowing urgency.

---

### **3. Effort (Quick Wins)**

| Condition | Score Impact |
|----------|--------------|
| Task duration < 2 hours | **+15** |

Helps encourage momentum with quick wins while still prioritizing deadlines.

---

# ❓ Why Is “Urgency” Weighted More Than “Effort”?

This design choice ensures that:
- Critical tasks are **never** overshadowed by small, easy ones  
- Deadline management remains the **dominant factor**  
- Users avoid penalties or failures due to procrastinating on urgent tasks

**In short:**  
A difficult but urgent task will *always* outrank an easy, non-urgent one.

---

# ⭐ Features

### ✅ **Smart Scoring**
Automatically calculates a dynamic priority score using urgency, importance, and effort.

### 🔄 **Multiple Sorting Modes**
Available in the frontend:
- **Smart Balance (Default)**
- **Deadline Driven**
- **Fastest Wins**

### 🎨 **Visual Feedback**
Color-coded task cards for immediate understanding:
- 🔴 **High Priority**
- 🟡 **Medium Priority**
- 🟢 **Low Priority**

---
