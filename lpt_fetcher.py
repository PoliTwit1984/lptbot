import glob
import os
import random
import textwrap
from string import ascii_letters
import datetime

import praw
import tweepy
from PIL import Image, ImageDraw, ImageFont

import config

client = tweepy.Client(config.bearer_token, config.consumer_key,
                       config.consumer_secret, config.access_token, config.access_token_secret)
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


class LPTFetcher:
    def __init__(self, sub="lifeprotips", time_span="week", limit=10):
        self.time_span = time_span
        self.limit = limit
        self.sub = sub
        self.reddit_key = "4PuhlbITTvHWOVdwcD3cyw"
        self.reddit_secret = "zGtU9KorcWW0nfPJt7CARxqWp8mWNA"
        self.user_agent = "politwit"
        self.reddit = praw.Reddit(
            client_id=self.reddit_key, client_secret=self.reddit_secret, user_agent=self.user_agent)

    def get_lpts(self):

        x = 1
        for submission in self.reddit.subreddit(self.sub).top(time_filter=self.time_span, limit=self.limit):
            text = submission.title
            print(submission.score)
            author = submission.author
            print(submission.url)
            # Open image
            img = Image.open(fp='background2.jpg', mode='r')
            # Load custom font
            font = ImageFont.truetype(font='AllerDisplay.ttf', size=52)
            # Create DrawText object
            draw = ImageDraw.Draw(im=img)
            # Calculate the average length of a single character of our font.
            # Note: this takes into account the specific font and font size.
            avg_char_width = sum(font.getsize(
                char)[0] for char in ascii_letters) / len(ascii_letters)
            # Translate this average length into a character count
            max_char_count = int(img.size[0] * .618 / avg_char_width)
            # Create a wrapped text object using scaled character count
            text = textwrap.fill(text=f"{text}", width=max_char_count)
            # Add text to the image
            draw.text(xy=(img.size[0]/2, img.size[1] / 2),
                      text=text, font=font, fill='white', anchor='mm')
            # view the result
            filename = f"{x}.jpg"
            img.save(filename)
            x = x + 1
        return

    def tweet_lpt_image(self, tweet_text="Life Pro Tip of the Day.", del_file=True):
        file_list = []
        for file in glob.glob("*.jpg"):
            file_list.append(file)
        ''' Make sure there are files in the directory to tweet'''
        if len(file_list) > 0:

            random_image = random.choice(file_list)
            print(random_image)

            media = api.media_upload(random_image)
            tweet_info = api.update_status(
                status=tweet_text, media_ids=[media.media_id])
            date_posted = datetime.datetime.now()
            if del_file:
                os.remove(random_image)
            else:
                lpt_tweet_file = open("lpt_tweet_file.txt", "a")
                lpt_tweet_file.write(f"{date_posted}, {tweet_info.id}\n")

            tweeted = True
            print(tweet_info)
            print(tweet_info.id)

        else:
            print("No more images to tweet. Please add more images.")
            tweeted = False

        return tweeted


r = LPTFetcher(sub="lifeprotips", time_span="all", limit=365)

r.tweet_lpt_image(
    tweet_text="Make your life easier by using #LifeProTips #LifeProTipofTheDay #lpt", del_file=True)


# 'all_awardings', 'allow_live_comments', 'approved_at_utc', 'approved_by', 'archived', 'author', 'author_flair_background_color', 'author_flair_css_class', 'author_flair_richtext', 'author_flair_template_id', 'author_flair_text', 'author_flair_text_color', 'author_flair_type', 'author_fullname', 'author_is_blocked', 'author_patreon_flair', 'author_premium', 'award', 'awarders', 'banned_at_utc', 'banned_by', 'can_gild', 'can_mod_post', 'category', 'clear_vote', 'clicked', 'comment_limit', 'comment_sort', 'comments', 'content_categories', 'contest_mode', 'created', 'created_utc', 'crosspost', 'delete', 'disable_inbox_replies', 'discussion_type', 'distinguished', 'domain', 'downs', 'downvote', 'duplicates', 'edit', 'edited', 'enable_inbox_replies', 'flair', 'fullname', 'gild', 'gilded', 'gildings', 'hidden', 'hide', 'hide_score', 'id', 'id_from_url', 'is_created_from_ads_ui', 'is_crosspostable', 'is_meta', 'is_original_content', 'is_reddit_media_domain', 'is_robot_indexable', 'is_self', 'is_video', 'likes', 'link_flair_background_color', 'link_flair_css_class', 'link_flair_richtext', 'link_flair_template_id', 'link_flair_text', 'link_flair_text_color', 'link_flair_type', 'locked', 'mark_visited', 'media', 'media_embed', 'media_only', 'mod', 'mod_note', 'mod_reason_by', 'mod_reason_title', 'mod_reports', 'name', 'no_follow', 'num_comments', 'num_crossposts', 'num_reports', 'over_18', 'parent_whitelist_status', 'parse', 'permalink', 'pinned', 'pwls', 'quarantine', 'removal_reason', 'removed_by', 'removed_by_category', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'secure_media', 'secure_media_embed', 'selftext', 'selftext_html', 'send_replies', 'shortlink', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_subscribers', 'subreddit_type', 'suggested_sort', 'thumbnail', 'thumbnail_height', 'thumbnail_width', 'title', 'top_awarded_type', 'total_awards_received', 'treatment_tags', 'unhide', 'unsave', 'ups', 'upvote', 'upvote_ratio', 'url', 'user_reports', 'view_count', 'visited', 'whitelist_status', 'wls']
# ['STR_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_chunk', '_comments_by_id', '_fetch', '_fetch_data', '_fetch_info', '_fetched', '_kind', '_reddit', '_reset_attributes', '_safely_add_arguments', '_url_parts', '_vote', 'all_awardings', 'allow_live_comments', 'approved_at_utc', 'approved_by', 'archived', 'author', 'author_flair_background_color', 'author_flair_css_class', 'author_flair_richtext', 'author_flair_template_id', 'author_flair_text', 'author_flair_text_color', 'author_flair_type', 'author_fullname', 'author_is_blocked', 'author_patreon_flair', 'author_premium', 'award', 'awarders', 'banned_at_utc', 'banned_by', 'can_gild', 'can_mod_post', 'category', 'clear_vote', 'clicked', 'comment_limit', 'comment_sort', 'comments', 'content_categories', 'contest_mode', 'created', 'created 'is_video', 'likes', 'link_flair_background_color', 'link_flair_css_class', 'link_flair_richtext', 'link_flair_template_id', 'link_flair_text', 'link_flair_text_color', 'link_flair_type', 'locked', 'mark_visited', 'media', 'media_embed', 'media_only', 'mod', 'mod_note', 'mod_reason_by', 'mod_reason_title', 'mod_reports', 'name', 'no_follow', 'num_comments', 'num_crossposts', 'num_reports', 'over_18', 'parent_whitelist_status', 'parse', 'permalink', 'pinned', 'pwls', 'quarantine', 'removal_reason', 'removed_by', 'removed_by_category', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'secure_media', 'secure_media_embed', 'selftext', 'selftext_html', 'send_replies', 'shortlink', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_subscribers', 'subreddit_type', 'suggested_sort', 'thumbnail', 'thumbnail_height', 'thumbnail_width', 'title', 'top_awarded_type', 'total_awards_received', 'treatment_tags', 'unhide', 'unsave', 'ups', 'upvote', 'upvote_ratio', 'url', 'user_reports', 'view_count', 'visited', 'whitelist_status', 'wls'
