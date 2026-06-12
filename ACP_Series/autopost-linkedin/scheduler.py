# pyrefly: ignore [missing-import]
import schedule
import time
from main import run

schedule.every().day.at("09:30").do(run)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(30)