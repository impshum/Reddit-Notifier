import praw
import time


client_id = 'XXXX'
client_secret = 'XXXX'
reddit_user = 'XXXX'
reddit_pass = 'XXXX'
user_agent = 'Find it! (by /u/impshum)'


send_to = 'XXXX'
target_subreddit = 'XXXX'
target_keywords = ['XXXX', 'XXXX', 'XXXX']

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=reddit_user,
                     password=reddit_pass)

start_time = time.time()

for submission in reddit.subreddit(target_subreddit).stream.submissions():
    title = submission.title
    for key in target_keywords:
        if start_time > submission.created_utc and key in title:
            print('Found one!')
            author = submission.author
            sub = submission.subreddit
            date = time.strftime("%B %d %Y %H:%M:%S", time.gmtime(submission.created_utc))
            body = submission.selftext
            link = submission.permalink
            msg = f'u/{author}\n\nr/{sub}\n\n{date}\n\n{body}\n\nhttps://reddit.com/{link}'
            reddit.redditor(send_to).message(title, msg)
