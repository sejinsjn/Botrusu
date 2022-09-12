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

event_hook = Webhook("https://discord.com/api/webhooks/1018967006764081162/tKCCPstVLrdaEoRpljmBTeEf-dSOByiMykOs9jCHwXGRgBr2-iY9KkZEFphy6BqF5r5y")

redeem_hook = Webhook("https://discord.com/api/webhooks/1018943521694163036/8uY04Wn3L3ZT72CRE6df7LJNW9iPNKrZIXwls61sespzkmNSYdmolrt1r98WeDf5I8ZR")

info_hook = Webhook("https://discord.com/api/webhooks/1018977913128894575/iNhufVdDb3WvK4NDylDOKFl-UnUMol7KyZB8yDChvEjKVCKax-MSZvcN_3GdeTwSkPaR")

pex_hook = Webhook("https://discord.com/api/webhooks/1018978349386838037/5jtH6Zlx_f-qpLcIaN8fz5m75a8a51plvXUdCOWSmLtoExLKz25kpB1fxQk0Ekr-rbcm")


ptrades = reddit.subreddit("pokemontrades")
pex = reddit.subreddit("Pokemonexchange")

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

def get_ptrades():
  for submission in ptrades.stream.submissions(skip_existing=True):
    if(str(submission.link_flair_text) == "Event"):
      event_hook.send(embed=create_embed(submission))
    if(str(submission.link_flair_text) == "Redeem"):
      redeem_hook.send(embed=create_embed(submission))
    if(str(submission.link_flair_text) == "Info"):
      redeem_hook.send(embed=create_embed(submission))

def get_pex():
  for submission in pex.stream.submissions(skip_existing=True):
    if(str(submission.link_flair_text) == "Selling Virtual"):
      pex_hook.send(embed=create_embed(submission))

def create_embed(submission):
  embed = Embed(
    title=submission.title,
    description=submission.selftext,
    timestamp='now',
    url=submission.url
  )
  embed.set_author(name=str(submission.author))
  return embed
      
ptrades_thread = threading.Thread(target=get_ptrades)
pex_thread = threading.Thread(target=get_ptrades)

ptrades_thread.start()
pex_thread.start()