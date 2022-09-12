import praw
import threading 
import os
from dhooks import Webhook, Embed
from keep_alive import keep_alive

reddit = praw.Reddit(
  client_id = os.getenv("client_id"),
  client_secret = os.getenv("client_secret"),
  username = os.getenv("username"),
  password = os.getenv("password"),
  user_agent = "<Botrusu>"
)

ptrades_event_hook = Webhook("https://discord.com/api/webhooks/1018654699194425445/H81oXFw2_qYqaAmiBhamtY2DghFh3UgwCIhRlrJtsdzVV3kEm_6x4tR1XRqn9iZ3z5hd")

ptrades_redeem_hook = Webhook("https://discord.com/api/webhooks/1018943521694163036/8uY04Wn3L3ZT72CRE6df7LJNW9iPNKrZIXwls61sespzkmNSYdmolrt1r98WeDf5I8ZR")


ptrades = reddit.subreddit("pokemontrades")

keep_alive()

"""
def get_comments():
  for comment in subreddit.stream.comments(skip_existing=True):
    embed = Embed(
      description=comment.body,
      timestamp='now',
      author=comment.author,
      url=comment.permalink
    )
    hook.send(embed=embed)
"""

def get_event_submissions_ptrades():
  for submission in ptrades.stream.submissions(skip_existing=True):
    if(str(submission.link_flair_text) == "Event"):
      embed = Embed(
        title=submission.title,
        description=submission.selftext,
        timestamp='now',
        url=submission.url
      )
      embed.set_author(name=str(submission.author))
      ptrades.send(embed=embed)

def get_redeem_submissions_ptrades():
  for submission in ptrades.stream.submissions(skip_existing=True):
    if(str(submission.link_flair_text) == "Redeem"):
      embed = Embed(
        title=submission.title,
        description=submission.selftext,
        timestamp='now',
        url=submission.url
      )
      embed.set_author(name=str(submission.author))
      ptrades.send(embed=embed)


event = threading.Thread(target=get_event_submissions_ptrades) 
redeem = threading.Thread(target=get_redeem_submissions_ptrades)

event.start()
redeem.start()