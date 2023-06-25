import instaloader
import json
import boto3
from itertools import takewhile, dropwhile
from datetime import datetime

# TODO: bucket name 수정 필요
bucket_name = "may-be-clean"

def savePostsToS3(posts_json, bucket_name, object_key):
    # TODO: profile 적용 필요
    session = boto3.Session(profile_name='hwangonjang')
    # Create an S3 client
    s3 = session.client('s3')

    # Upload the JSON data to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=posts_json.encode('utf-8'),
        ContentType='application/json'
    )

def list_instagram_posts_by_username(username):
    # create an instance of Instaloader class
    loader = instaloader.Instaloader()

    # get profile information of the user
    profile = instaloader.Profile.from_username(loader.context, username)
    # create a generator for posts of the user
    posts = profile.get_posts()

    profile_info = {
        "userid": profile.userid,
        "username": profile.username,
        "external_url": profile.external_url,
        "followees": profile.followees,
        "followers": profile.followers,
    }

    # create a generator for posts of the user within the specified date range
    SINCE = datetime(2099, 12, 31)
    UNTIL = datetime(2022, 12, 23)

    # filtered_posts = [post for post in posts if post.mediaid > last_media_id]

    instagram_posts = []
    # iterate over the filtered generator to get information for each post
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    # for post in posts:
        # access attributes of the post object to get information
        post_id = post.mediaid
        caption = post.caption
        like_count = post.likes
        comment_count = post.comments
        location = post.location
        posted_at = post.date_local
        is_video = post.is_video
        media_urls = []

        # check if the post has pictures
        if is_video:
            media_urls.append(post.video_url)
        else:
            init = False
            # iterate over each picture in the post and get its URL
            for pic in post.get_sidecar_nodes():
                init = True
                media_urls.append(pic.display_url)
            if not init:
                media_urls.append(post.url)

        instagram_posts.append({
            "postId": post_id,
            "caption": caption,
            "location": location,
            "mediaUrls": media_urls,
            "isVideo": is_video,
            "postedAt": str(posted_at).split('+')[0],
            "commentCount": comment_count,
            "likeCount": like_count,
        })

    posts = []
    page = len(instagram_posts) // 10
    if page == 0:
        posts.append(instagram_posts)
    else:
        for i in range(page):
            size = i * 10 + 10
            posts.append(instagram_posts[i * 10:size])

    # convert the list to a JSON array
    profile_json = json.dumps({"profile": profile_info}, ensure_ascii=False, indent=4)
    posts_json = [json.dumps({"posts": post}, ensure_ascii=False, indent=4) for post in posts]

    # add s3 json object
    object_key = f"instagram/{username}/profile/profile.json"
    savePostsToS3(profile_json, bucket_name, object_key)

    for i in range(len(posts_json), 0, -1):
        # print(posts_json[i])
        object_key = f"instagram/{username}/post/posts{i}.json"
        savePostsToS3(posts_json[i-1], bucket_name, object_key)