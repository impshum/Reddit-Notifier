import os
import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


email_server = 'smtp.gmail.com'
email_port = 587
sender_name = 'Notifier <email@email.com>'
email_account = 'XXXX'
email_password = 'XXXX'

client_id = 'XXXX'
client_secret = 'XXXX'
user_agent = 'Find it! (by /u/impshum)'


send_to = ['XXXX', 'XXXX']
target_subreddit = 'all'
target_keywords = ['XXXX', 'XXXX', 'XXXX']


def mailer(title, body, date, author, sub, link):
    try:
        mail = smtplib.SMTP(email_server, email_port)
        mail.ehlo()
        mail.starttls()
        mail.login(email_account, email_password)
        for send_to_one in send_to:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = title
            msg['From'] = sender_name
            msg['To'] = send_to_one
            text = '{}\n\nSubmitted {} by /u/{}\nVia https://reddit.com/r/{} https://reddit.com{}'.format(
                body, str(date), author, sub, link)
            html = "<html><head></head><body><p><strong>{}</strong><br><br>{}<br><br>Submitted {} by <a href='https://reddit.com/u/{}'>/u/{}</a><br>Via <a href='https://reddit.com/r/{}'>/r/{}</a> (<a href='https://reddit.com{}'>Link</a>)</p></body></html>".format(
                title, body, str(date), author, author, sub, sub, link)
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            print('Sending mail to {}'.format(send_to_one))
            mail.sendmail(email_account, send_to_one, msg.as_string())
        mail.quit()
    except Exception as e:
        print(e)


reddit = praw.Reddit(user_agent=user_agent,
                     client_id=client_id, client_secret=client_secret)

subreddit = reddit.subreddit(target_subreddit)
start_time = time.time()
for submission in subreddit.stream.submissions():
    title = submission.title
    for key in target_keywords:
        if key in title:
            if start_time < submission.created_utc:
                print('Found one!')
                author = submission.author
                sub = submission.subreddit
                date = time.strftime("%b %d %Y at %H:%M:%S",
                                     time.gmtime(submission.created_utc))
                body = submission.selftext
                link = submission.permalink
                mailer(title, body, date, author, sub, link)
