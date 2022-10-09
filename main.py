from discord.ext import tasks
from discord.ext import commands
import discord
import os
import asyncpraw
from keep_alive import keep_alive
from datetime import datetime
from replit import db

TOKEN = os.getenv('token')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

db["annoyuser"] = "nobody"
db["ssuser"] = "nobody"
#db["stalk"] = ["Theduskwolf", "KaitoGL", "SwiftGoten", "hgem0406", "sparrowcount", "serenity-as-ice", "bwo0", "OnePointPi", "CrazyNek0"]


#commands
@bot.command(pass_context=True)
async def annoy(ctx, arg):
    db["annoyuser"] = arg.replace(">", "").replace("<", "").replace(
        "@", "").replace(" ", "").strip()


@bot.command(pass_context=True)
async def samsungsmile(ctx, arg):
    db["ssuser"] = arg.replace(">",
                               "").replace("<",
                                           "").replace("@",
                                                       "").replace(" ",
                                                                   "").strip()


@bot.command(pass_context=True)
async def stalk(ctx, arg):
    if str(arg) == "list":
        list = '\n'.join(db["stalk"])
        await ctx.send(list)
    else:
        stalk = db["stalk"]
        stalk.append(str(arg))
        db["stalk"] = stalk
        await ctx.send("Im stalking " + arg + " now!")


@bot.command(pass_context=True)
async def unstalk(ctx, arg):
    stalk = db["stalk"]
    for s in stalk:
        if s == arg:
            stalk.remove(arg)
            db["stalk"] = stalk
            await ctx.send("Im not stalking " + arg + " anymore! :(")
            return
    await ctx.send("Who is " + arg + "? :thinkingeyes:")


@bot.event
async def on_message(message):
    if str(message.author.id) == str(db["annoyuser"]):
        print("Hello there!" + str(message.author.id))
        await message.reply('Hello there!', mention_author=True)
    else:
        if str(message.author.id) == str(db["ssuser"]):
            print("Samsungsmile: " + str(message.author.id))
            await message.add_reaction(':samsungsmile:1018574192020553830')
        else:
            await bot.process_commands(message)


#Reddit updates
def create_embed(submission):
    embed = discord.Embed(title=submission.title,
                          description=submission.selftext,
                          timestamp=datetime.now(),
                          url=submission.url)
    embed.set_author(name=str(submission.author))
    return embed


def create_comment_embed(comment):
    embed = discord.Embed(title=str(comment.author),
                          description=str(comment.body),
                          timestamp=datetime.now(),
                          url="https://www.reddit.com" + comment.permalink)
    return embed


@tasks.loop(seconds=1)
async def test_comments():
    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="<Botrusu>")

    subreddit = await reddit.subreddit("AskReddit")
    async for comment in subreddit.stream.comments(skip_existing=True):
        channel = bot.get_channel(1019954852173987942)
        await channel.send(embed=create_comment_embed(comment))


@tasks.loop(seconds=1)
async def test_submissions():
    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="<Botrusu>")

    subreddit = await reddit.subreddit("askreddit")
    async for submission in subreddit.stream.submissions(skip_existing=True):
        channel = bot.get_channel(1019954852173987942)
        await channel.send(embed=create_embed(submission))


@tasks.loop(seconds=1)
async def ptrades_posts():
    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="<Botrusu>")

    subreddit = await reddit.subreddit("pokemontrades")
    async for submission in subreddit.stream.submissions(skip_existing=True):
        if (str(submission.link_flair_text) == "Event"):
            channel = bot.get_channel(1018966932092895323)
            await channel.send(embed=create_embed(submission))
        if (str(submission.link_flair_text) == "Redeem"):
            channel = bot.get_channel(1018943497425928302)
            await channel.send(embed=create_embed(submission))
        if (str(submission.link_flair_text) == "Info"):
            channel = bot.get_channel(1018977894208372777)
            await channel.send(embed=create_embed(submission))


@tasks.loop(seconds=1)
async def pex_posts():
    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="<Botrusu>")

    subreddit = await reddit.subreddit("Pokemonexchange")
    async for submission in subreddit.stream.submissions(skip_existing=True):
        if (str(submission.link_flair_text) == "Selling Virtual"):
            channel = bot.get_channel(1018978331665903716)
            await channel.send(embed=create_embed(submission))


@tasks.loop(seconds=1)
async def stalking_ptrades():
    #["Theduskwolf", "KaitoGL", "SwiftGoten", "hgem0406", "sparrowcount", "sejin_mb", "serenity-as-ice", "bwo0", "OnePointPi", "CrazyNek0"]

    reddit = asyncpraw.Reddit(client_id=os.getenv("client_id"),
                              client_secret=os.getenv("client_secret"),
                              user_agent="<Botrusu>")

    subreddit = await reddit.subreddit("pokemontrades")
    async for comment in subreddit.stream.comments(skip_existing=True):
        bad_ppl = db["stalk"]
        for bad in bad_ppl:
            print(bad)
            if str(bad) == str(comment.author):
                channel = bot.get_channel(1018984167284949023)
                await channel.send(embed=create_comment_embed(comment))


@bot.event
async def on_ready():
    ptrades_posts.start()
    pex_posts.start()
    stalking_ptrades.start()
    #test_submissions.start()
    #test_comments.start()
    keep_alive()


bot.run(TOKEN)
