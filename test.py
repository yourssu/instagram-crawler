from instagram_crawler import list_instagram_posts_by_username

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from datetime import datetime

scheduler = BackgroundScheduler()

profiles = [
    ("숭실대학교 인권위원회", "ssu_huri", "https://www.instagram.com/ssu_huri/")
]


def crawl_job():
    for profile in profiles:
        print(f"{profile[0]} 크롤링 시작...{datetime.now()}")
        list_instagram_posts_by_username(profile[1], profile[2])


if __name__ == "__main__":
    crawl_job()
