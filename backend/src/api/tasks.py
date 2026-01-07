from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database import get_session
from src.models.models import Task, User
from src.api.auth_middleware import verify_jwt

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def get_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(verify_jwt)
):
    statement = select(Task).where(Task.user_id == user_id)
    results = session.exec(statement).all()
    return results

@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: Task,
    session: Session = Depends(get_session),
    user_id: int = Depends(verify_jwt)
):
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: Task,
    session: Session = Depends(get_session),
    user_id: int = Depends(verify_jwt)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        if key != "id" and key != "user_id":
            setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_complete(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(verify_jwt)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(verify_jwt)
):
    # Use select to ensure we find the task and verify ownership
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return None
