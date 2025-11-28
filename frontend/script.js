let currentTasks = []; // Store tasks here so we can re-sort them

async function analyzeTasks() {
    const inputField = document.getElementById('taskInput');
    const resultsContainer = document.getElementById('resultsContainer');
    
    resultsContainer.innerHTML = '<p>Analyzing...</p>';

    try {
        const tasks = JSON.parse(inputField.value);

        const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(tasks)
        });

        if (!response.ok) throw new Error('Server Error');

        // Save the data to our global variable
        currentTasks = await response.json();
        
        // Trigger the sort function to display them
        resortTasks();

    } catch (error) {
        console.error(error);
        resultsContainer.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
    }
}

function resortTasks() {
    const strategy = document.getElementById('sortStrategy').value;
    let sorted = [...currentTasks]; // Make a copy

    if (strategy === 'deadline') {
        // Sort by Due Date (earliest first)
        sorted.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    } else if (strategy === 'effort') {
        // Sort by Effort (lowest hours first)
        sorted.sort((a, b) => a.estimated_hours - b.estimated_hours);
    } else {
        // Smart Balance (Score High to Low)
        sorted.sort((a, b) => b.score - a.score);
    }

    displayResults(sorted);
}

function displayResults(tasks) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = ''; 

    tasks.forEach(task => {
        const div = document.createElement('div');
        
        let priorityClass = 'priority-low';
        // Use the backend score for coloring, regardless of sort order
        if (task.score >= 50) priorityClass = 'priority-high';
        else if (task.score >= 20) priorityClass = 'priority-medium';

        div.className = `task-card ${priorityClass}`;
        
        // Add explanation if it exists (from the suggest endpoint logic), or generic
        const explanation = task.explanation ? `<br><em>${task.explanation}</em>` : '';

        div.innerHTML = `
            <div class="task-header">
                <span class="task-title">${task.title}</span>
                <span class="task-score">Score: ${task.score}</span>
            </div>
            <div class="task-details">
                Due: ${task.due_date} | Hrs: ${task.estimated_hours} ${explanation}
            </div>
        `;
        container.appendChild(div);
    });
}

function loadSampleData() {
    const sample = [
        { "title": "Submit Assignment", "due_date": "2025-11-29", "importance": 10, "estimated_hours": 4 },
        { "title": "Buy Groceries", "due_date": "2025-12-05", "importance": 3, "estimated_hours": 1 },
        { "title": "Overdue Project", "due_date": "2025-11-01", "importance": 8, "estimated_hours": 5 },
        { "title": "Quick Fix", "due_date": "2025-12-01", "importance": 4, "estimated_hours": 0.5 }
    ];
    document.getElementById('taskInput').value = JSON.stringify(sample, null, 4);
}