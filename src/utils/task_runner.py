import subprocess
from .models import RPATask, session
from datetime import datetime, timezone

def run_task(task_id):
    task = session.query(RPATask).get(task_id)
    if not task:
        print("Task not found.")
        return

    # Set the path to the entry point file
    entry_point = task.code_entry_point
    log_file = task.log_file

    try:
        # Run the task and capture output
        with open(log_file, 'w') as log:
            result = subprocess.run(["python", entry_point], stdout=log, stderr=log, text=True)
        
        # Update task status based on result
        task.status = "running" if result.returncode == 0 else "failed"
        task.last_run_at = datetime.now(timezone.utc())
        session.commit()

        # Provide feedback on the task execution
        print(f"Task '{task.name}' completed with status: {task.status}")
        if task.status == "failed":
            print("Check the log file for details:", log_file)
    except Exception as e:
        print("Failed to run task:", str(e))
        task.status = "failed"
        session.commit()
