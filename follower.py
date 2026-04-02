from instagrapi import Client
import random as r
import time
import schedule

username = "your_username"
password = "your_password"

tags = ["#yourtag", "#yourtag2", "#yourtag3"]

comments = ["Great post!", "I love this!", "Awesome content!"]

def search_tag(tag):
    cl = Client()
    cl.login(username, password)
    media_pk = cl.search_posts_by_tag(tag)
    return media_pk

def like_post(media_pk):
    cl = Client()
    cl.login(username, password)
    cl.like(media_pk)

def comment_post(media_pk):
    cl = Client()
    cl.login(username, password)
    cl.comment(media_pk, r.choice(comments))

def follow_user(user_id):
    cl = Client()
    cl.login(username, password)
    cl.follow(user_id)

def unfollow_user(user_id):
    cl = Client()
    cl.login(username, password)
    cl.unfollow(user_id)        

    num_interaction_posts = r.randint(1,5)
    time.sleep(r.randint(2000, 7000)/1000)
    tag_choice = r.choice(tags)
    hashtag_posts = client.hashtag_medias_recent(tag_choice)
    print(f"searched tag ({tag_choice}) ----")


