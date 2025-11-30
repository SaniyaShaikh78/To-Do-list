from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Task
from app import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/tasks')
def view_tasks():
    try:
        tasks = Task.query.all()
    except Exception:
        tasks = []
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/tasks/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if not title:
        flash('Title is required', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added', 'success')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Done'
    else:
        task.status = 'Pending'
    db.session.commit()
    flash(f'Task status changed to {task.status}', 'info')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/tasks/clear', methods=['POST'])
def clear_tasks():
    try:
        num = Task.query.delete()
        db.session.commit()
        flash(f'Cleared {num} tasks', 'info')
    except Exception:
        db.session.rollback()
        flash('Could not clear tasks', 'danger')
    return redirect(url_for('tasks.view_tasks'))
