# tasks.py in one of your apps

from celery import shared_task
from add_data import main
from datetime import datetime

@shared_task()
def daily_update_data():
    print(f"Updating Database from Latest update on datausa.io at {datetime.now()}")
    main()
