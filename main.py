from dhooks import Webhook
import praw
import os

hook = Webhook("https://discord.com/api/webhooks/1018654699194425445/H81oXFw2_qYqaAmiBhamtY2DghFh3UgwCIhRlrJtsdzVV3kEm_6x4tR1XRqn9iZ3z5hd")


reddit = praw.Reddit(
  client_id = os.getenv("client_id"),
  client_secret = os.getenv("client_secret"),
  username = os.getenv("username"),
  password = os.getenv("password"),
  user_agent = "<Botrusu>"
)

subreddit = reddit.subreddit("pokemontrades")

for comment in subreddit.stream.comments(skip_existing=True):
    hook.send(comment.body)