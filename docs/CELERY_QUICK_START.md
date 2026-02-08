# Celery Quick Start Guide

## 🚀 Quick Setup (Development)

### 1. Install Redis (One-time setup)

**Windows (WSL - Recommended):**
```bash
wsl --install
# In WSL terminal:
sudo apt update && sudo apt install redis-server
sudo service redis-server start
```

**Windows (Docker - Alternative):**
```bash
docker run -d -p 6379:6379 redis:latest
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

### 2. Verify Redis is Running
```bash
redis-cli ping
# Should return: PONG
```

### 3. Run the Application

**Terminal 1 - Django:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
# Windows
celery -A config worker --loglevel=info --pool=solo

# Linux/Mac
celery -A config worker --loglevel=info
```

**Terminal 3 - Celery Beat (Optional - for scheduled tasks):**
```bash
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## 📝 Creating a Task

### 1. Create tasks.py in your app:

```python
# apps/myapp/tasks.py
from celery import shared_task

@shared_task
def my_async_task(param1, param2):
    """Your task description."""
    # Your code here
    return "Task completed!"
```

### 2. Use the task:

```python
# In your views or services
from apps.myapp.tasks import my_async_task

# Execute asynchronously
result = my_async_task.delay(param1="value1", param2="value2")

# Execute with delay (in seconds)
my_async_task.apply_async(
    args=["value1", "value2"],
    countdown=60  # Execute in 60 seconds
)
```

## 🔄 Periodic Tasks

### Via Django Admin:

1. Go to: http://localhost:8000/admin/
2. Navigate to: **Periodic Tasks** → **Add Periodic Task**
3. Fill in:
   - **Name**: Descriptive name
   - **Task**: Select your task (e.g., `apps.myapp.tasks.my_async_task`)
   - **Interval/Crontab**: Choose schedule type
   - **Arguments**: `["arg1", "arg2"]` (JSON format)
   - **Enabled**: ✓

### Common Crontab Schedules:

- Every day at 9 AM: `0 9 * * *`
- Every Monday at 8 AM: `0 8 * * 1`
- Every hour: `0 * * * *`
- Every 30 minutes: `*/30 * * * *`

## 🧪 Testing

### Test in Django Shell:
```python
python manage.py shell

>>> from apps.users.tasks import test_celery_task
>>> result = test_celery_task.delay()
>>> result.ready()  # Check if completed
True
>>> result.get()    # Get result
'Celery is working correctly!'
```

### Test Script:
```bash
python test_celery.py
```

## 🐛 Troubleshooting

### "Error 10061 connecting to localhost:6379"
→ Redis is not running. Start Redis server.

### Tasks not executing
1. Check Celery worker is running
2. Check Redis connection: `redis-cli ping`
3. Check worker logs for errors

### Windows "NotImplementedError: pool"
→ Use `--pool=solo` flag:
```bash
celery -A config worker --loglevel=info --pool=solo
```

## 📚 More Information

See `docs/CELERY_SETUP.md` for detailed documentation.

## ✅ Verification Checklist

- [ ] Redis installed and running
- [ ] `redis-cli ping` returns PONG
- [ ] Django server running
- [ ] Celery worker running
- [ ] Test task executes successfully
- [ ] (Optional) Celery beat running for periodic tasks

## 🎯 Common Use Cases

### Send Email Asynchronously:
```python
@shared_task
def send_email_task(user_id, subject, message):
    from django.core.mail import send_mail
    from apps.users.models import CustomUser
    
    user = CustomUser.objects.get(id=user_id)
    send_mail(subject, message, 'noreply@pratik.gf', [user.email])
```

### Process Data in Background:
```python
@shared_task
def process_large_dataset(dataset_id):
    # Long-running data processing
    pass
```

### Scheduled Cleanup:
```python
@shared_task
def cleanup_old_records():
    # Delete old records
    pass
```

Configure in Django Admin as periodic task with crontab: `0 2 * * *` (daily at 2 AM)
