"""
Test tasks for verifying Celery configuration.

These tasks can be used to test that Celery is properly configured
and working correctly.
"""
from celery import shared_task
import time


@shared_task
def add(x, y):
    """
    Simple addition task for testing.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        Sum of x and y
    """
    return x + y


@shared_task
def multiply(x, y):
    """
    Simple multiplication task for testing.
    
    Args:
        x: First number
        y: Second number
        
    Returns:
        Product of x and y
    """
    return x * y


@shared_task
def long_running_task(duration=5):
    """
    Simulates a long-running task.
    
    Args:
        duration: Number of seconds to sleep
        
    Returns:
        Success message
    """
    time.sleep(duration)
    return f"Task completed after {duration} seconds"


@shared_task
def hello_world():
    """
    Simple hello world task.
    
    Returns:
        Hello world message
    """
    return "Hello from Celery!"
