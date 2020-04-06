import praw
import time
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    reddit_user = config['REDDIT']['reddit_user']
    reddit_pass = config['REDDIT']['reddit_pass']
    reddit_client_id = config['REDDIT']['reddit_client_id']
    reddit_client_secret = config['REDDIT']['reddit_client_secret']
    target_subreddits = config['SETTINGS']['target_subreddits'].replace(
        ',', '+')
    target_keywords = config['SETTINGS']['target_keywords'].split(',')
    target_user = config['SETTINGS']['target_user']

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         username=reddit_user,
                         password=reddit_pass,
                         user_agent='Find it! (by /u/impshum)')

    for submission in reddit.subreddit(target_subreddits).stream.submissions(skip_existing=False):
        title = submission.title
        for key in target_keywords:
            if key in title:
                msg_title = title if len(title) <= 100 else title[:97] + "..."
                author = submission.author
                sub = submission.subreddit
                body = submission.selftext
                link = submission.permalink
                date = time.strftime(
                    "%B %d %Y %H:%M", time.gmtime(submission.created_utc))
                msg = f'{date}\n\nu/{author} → r/{sub}\n\n{body}\n\n[link](https://reddit.com/{link})'
                reddit.redditor(target_user).message(msg_title, msg)
                print(title)


if __name__ == '__main__':
    main()
