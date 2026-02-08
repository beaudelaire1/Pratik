"""Test script to verify Celery configuration."""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.celery import app

# Autodiscover tasks
app.autodiscover_tasks()

print("✓ Celery app loaded successfully!")
print(f"✓ Broker: {app.conf.broker_url}")
print(f"✓ Backend: {app.conf.result_backend}")
print("\nRegistered tasks:")
for task in sorted(app.tasks.keys()):
    if not task.startswith('celery.'):
        print(f"  - {task}")
