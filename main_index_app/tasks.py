# tasks.py in one of your apps

from celery import shared_task

@shared_task()
def daily_update_data():
    print("This is the task that runs every day!")
