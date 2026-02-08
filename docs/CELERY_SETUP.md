# Celery Setup and Usage Guide

## Overview

Celery is configured for asynchronous task processing in the PRATIK platform. This allows for background processing of tasks like sending notifications, processing data, and scheduled periodic tasks.

## Installation

The following packages have been installed:
- `celery>=5.6,<6.0` - Distributed task queue
- `redis>=7.1,<8.0` - Message broker and result backend
- `django-celery-beat>=2.8,<3.0` - Database-backed periodic tasks

## Configuration

### Settings (config/settings.py)

```python
# Celery broker and backend
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Task serialization
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Timezone
CELERY_TIMEZONE = 'America/Cayenne'

# Periodic tasks scheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

### Celery App (config/celery.py)

The Celery app is configured in `config/celery.py` and automatically loaded when Django starts.

## Prerequisites

### Redis Server

Celery requires Redis to be running. 

**On Windows:**
1. **Option 1: WSL (Recommended)**
   ```bash
   # Install WSL if not already installed
   wsl --install
   
   # In WSL terminal:
   sudo apt update
   sudo apt install redis-server
   sudo service redis-server start
   ```

2. **Option 2: Docker**
   ```bash
   docker run -d -p 6379:6379 redis:latest
   ```

3. **Option 3: Windows Native (Memurai)**
   - Download Memurai (Redis-compatible) from https://www.memurai.com/
   - Install and start the service

**On Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis
```

### Verify Redis is Running

```bash
redis-cli ping
# Should return: PONG
```

## Running Celery

### Development

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A config worker --loglevel=info --pool=solo
```
*Note: `--pool=solo` is required on Windows*

**Terminal 3 - Celery Beat (for periodic tasks):**
```bash
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Production

Use a process manager like Supervisor or systemd:

```bash
# Worker
celery -A config worker --loglevel=info

# Beat
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Creating Tasks

### Basic Task

Create a `tasks.py` file in any Django app:

```python
# apps/notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(user_id, subject, message):
    """Send notification email to user."""
    from apps.users.models import CustomUser
    
    user = CustomUser.objects.get(id=user_id)
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@pratik.gf',
        recipient_list=[user.email],
        fail_silently=False,
    )
    return f"Email sent to {user.email}"
```

### Using Tasks

```python
# In your views or services
from apps.notifications.tasks import send_notification_email

# Call asynchronously
send_notification_email.delay(user_id=1, subject="Welcome", message="Hello!")

# Call with countdown (delay in seconds)
send_notification_email.apply_async(
    args=[1, "Reminder", "Don't forget!"],
    countdown=3600  # Execute in 1 hour
)
```

### Periodic Tasks

Periodic tasks are managed through the Django admin interface:

1. Go to Django Admin → Periodic Tasks
2. Click "Add Periodic Task"
3. Configure:
   - Name: Task name
   - Task: Select from registered tasks
   - Schedule: Crontab or Interval
   - Arguments: JSON format `[arg1, arg2]`
   - Keyword arguments: JSON format `{"key": "value"}`

Example crontab schedules:
- Every day at 9 AM: `0 9 * * *`
- Every Monday at 8 AM: `0 8 * * 1`
- Every hour: `0 * * * *`

## Task Organization

Organize tasks by domain:

```
core/
  tasks/
    __init__.py
    notification_tasks.py    # Notification-related tasks
    verification_tasks.py    # Document verification tasks
    calendar_tasks.py        # Calendar reminder tasks
```

## Monitoring

### Flower (Optional)

Install Flower for real-time monitoring:

```bash
pip install flower
celery -A config flower
```

Access at: http://localhost:5555

### Django Admin

Monitor periodic tasks in Django Admin:
- Periodic Tasks: View/edit scheduled tasks
- Periodic Task Results: View task execution history

## Testing

Test Celery tasks in development:

```python
# In Django shell
python manage.py shell

>>> from config.celery import debug_task
>>> result = debug_task.delay()
>>> result.ready()  # Check if task completed
>>> result.get()    # Get result
```

## Troubleshooting

### Redis Connection Error

```
Error: Error 10061 connecting to localhost:6379
```

**Solution:** Ensure Redis is running (see Prerequisites section)

### Tasks Not Executing

1. Check Celery worker is running
2. Check Redis connection
3. Check task is properly registered: `celery -A config inspect registered`
4. Check worker logs for errors

### Windows-Specific Issues

If you get "NotImplementedError: pool" on Windows:
```bash
celery -A config worker --loglevel=info --pool=solo
```

## Next Steps

1. Create task modules in `core/tasks/`
2. Implement notification tasks (Phase 5 of the spec)
3. Implement verification reminder tasks
4. Implement calendar reminder tasks
5. Configure periodic tasks in Django admin

## Resources

- [Celery Documentation](https://docs.celeryproject.org/)
- [Django-Celery-Beat Documentation](https://django-celery-beat.readthedocs.io/)
- [Redis Documentation](https://redis.io/documentation)
