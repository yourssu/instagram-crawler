from instagram_crawler import list_instagram_posts_by_username

profiles = [
    "plussu__63rd"
]

if __name__=="__main__":
    for profile in profiles:
        list_instagram_posts_by_username("profile")