from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import send_mass_email

def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(send_mass_email, 'interval', seconds=10)
    scheduler.add_job(send_mass_email, 'cron', hour=10, minute=30)
    scheduler.start()