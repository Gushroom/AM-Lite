import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from .models import RPATask, session

def create_task(task_name, entry_point_content):
    # Define the workspace and log file paths
    workspace_dir = f'workspaces/{task_name}'
    os.makedirs(workspace_dir, exist_ok=True)
    entry_point_path = os.path.join(workspace_dir, 'main.py')
    log_file_path = os.path.join(workspace_dir, 'task.log')
    
    # Write the entry point script to the workspace
    with open(entry_point_path, 'w') as file:
        file.write(entry_point_content)
    
    # Store task information in the database
    task = RPATask(
        name=task_name,
        workspace_dir=workspace_dir,
        code_entry_point=entry_point_path,
        interval=-1,
        status="idle",
        log_file=log_file_path,
    )
    session.add(task)
    session.commit()
    print(f"Task '{task_name}' created with workspace at '{workspace_dir}'.")
