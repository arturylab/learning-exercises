import schedule
import time


def day_hello():
    print("Hello, World! it's time for your scheduled task")


def fecth_news_headlines():
    print("Fetching news headlines...")


def backup_database():
    print("Backing up database...")


schedule.every().day.at("09:17").do(day_hello) # every day at 09:17
schedule.every(1).hour.do(fecth_news_headlines) # every 1 hour
schedule.every().day.at("09:19").do(backup_database) # every day at 09:19

while True:
    schedule.run_pending()
    time.sleep(1)
